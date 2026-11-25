#!/usr/bin/env node
import { spawn } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { mkdir, readFile, rm, stat } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { isInvokedDirectly } from "./direct.mjs";
import { markRunDir } from "./safety.mjs";
import { STDIO_DISCARD, STDIO_PIPE } from "./stdio-modes.mjs";

// 图片转换交给跨平台的 imgtool.py（Pillow）
const PY = process.env.PYTHON ?? (process.platform === "win32" ? "python" : "python3");
const here = path.dirname(fileURLToPath(import.meta.url));
const IMGTOOL = path.join(here, "imgtool.py");
export const LOVART_AGENT = path.join(here, "lovart_agent.py");

export const LOVART_DEFAULT_MODEL = "generate_image_nano_banana_pro";

let JSON_MODE = process.argv.includes("--json");
let billing = {};

function printHelp() {
  process.stdout.write("lovart.mjs — Lovart image generation\n\n  node scripts/lovart.mjs --out <file.png> --prompt \"<text>\" [flags]\n\n  --out <file>        输出 PNG 路径（必填）\n  --prompt <text>     提示词（必填，或用 --prompt-file）\n  --prompt-file <p>   从文件读提示词\n  --ref <file>        参考图，可重复。会先 upload 到 Lovart CDN 再作为 attachments\n  --aspect <r>        比例，如 2:3 / 16:9。⚠️ Lovart 没有比例参数，本 flag 只是\n                      把要求写进提示词，是软约束——出图后请自行校验\n  --model <tool>      锁定模型，默认 generate_image_nano_banana_pro\n                      可选 generate_image_seedream_v4_5 / generate_image_gpt_image_2 等\n  --mode <m>          fast(默认) | thinking\n  --lv <path>         可选包装脚本。已有 lv 优先于随包客户端\n  --query-mode       只查询计费模式和可免费使用的模型\n  --require-free     仅在 unlimited 模式且模型在白名单时出图\n  --timeout <sec>     单次 chat 超时，默认 300\n  --json              输出单行 JSON\n");
}

function fail(msg, kind = "error") {
  if (JSON_MODE) process.stdout.write(JSON.stringify({ status: "error", error: msg, error_kind: kind, ...billing }) + "\n");
  else process.stderr.write("ERROR " + (msg) + "\n");
  process.exit(kind === "invalid_args" ? 2 : 1);
}

function runProcess(cmd, args, timeoutSec, extraEnv) {
  return new Promise((res) => {
    let out = "", err = "", killed = false;
    const c = spawn(cmd, args, { stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE], env: extraEnv ? { ...process.env, ...extraEnv } : process.env });
    const t = timeoutSec ? setTimeout(() => { killed = true; c.kill("SIGKILL"); }, timeoutSec * 1000) : null;
    c.on("error", (e) => { if (t) clearTimeout(t); res({ code: -1, out, err: err + e }); });
    c.stdout.on("data", (d) => (out += d));
    c.stderr.on("data", (d) => (err += d));
    c.on("close", (code) => { if (t) clearTimeout(t); res({ code, out, err, killed }); });
  });
}

// lv 会把人类可读的行和 JSON 混在一起输出，取最后一个完整 JSON 对象
function lastJson(t) {
  const lines = t.trim().split(/\r?\n/);
  let end = lines.length;
  while (end > 0 && !lines[end - 1].trimEnd().endsWith("}")) end--;
  for (let start = end - 1; start >= 0; start--) {
    if (!lines[start].trimStart().startsWith("{")) continue;
    try { return JSON.parse(lines.slice(start, end).join("\n")); } catch {}
  }
  return null;
}

// Reads the file $HOME/.lovart/env as text. Does not execute it. Refuse credentials writable by group or others.
export function readLovartEnv(env = process.env) {
  const file = env.LOVART_ENV || path.join(homedir(), ".lovart", "env");
  const out = {};
  for (const key of ["LOVART_ACCESS_KEY", "LOVART_SECRET_KEY", "LOVART_BASE_URL"]) {
    if (key === "LOVART_BASE_URL" ? env[key] : env[key]?.trim()) out[key] = env[key];
  }
  if (!existsSync(file)) return out;
  const mode = statSync(file).mode & 0o777;
  if (mode & 0o022) {
    const error = new Error("Refusing to read " + (file) + ": mode " + (mode.toString(8)) + " allows group/other writes");
    error.code = "LOVART_ENV_MODE";
    throw error;
  }
  if (mode & 0o044) process.stderr.write("WARNING: Lovart credentials are readable by group/others; use chmod 600 on the credentials file.\n");
  let text = "";
  try { text = readFileSync(file, "utf8"); } catch { return out; }
  for (const line of text.split(/\n/)) {
    const match = line.match(/^\s*(?:export\s+)?(LOVART_ACCESS_KEY|LOVART_SECRET_KEY|LOVART_BASE_URL)\s*=\s*(.*)$/);
    if (!match || out[match[1]]?.trim()) continue;
    let value = match[2].trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
    out[match[1]] = value;
  }
  return out;
}

// --lv is explicit: it must exist. Otherwise an existing wrapper is kept, then the shipped client.
function resolveLv(explicit) {
  if (explicit) return existsSync(explicit) ? { cmd: explicit, args: [], env: {}, auth: "lv-wrapper" } : null;
  const cands = [process.env.LOVART_LV, path.join(homedir(), "tools", "lovart-skill", "lv")].filter(Boolean);
  for (const p of cands) if (existsSync(p)) return { cmd: p, args: [], env: {}, auth: "lv-wrapper" };
  if (!existsSync(LOVART_AGENT)) return null;
  return { cmd: PY, args: [LOVART_AGENT], env: readLovartEnv(), auth: "shipped-client" };
}

async function queryBilling(lv) {
  const result = await runProcess(lv.cmd, [...lv.args, "query-mode"], 20, lv.env);
  const data = result.code === 0 && lastJson(result.out);
  if (!data || !["fast", "unlimited"].includes(data.mode)) {
    fail("Lovart billing mode could not be verified. Check Lovart credentials and connectivity.", "billing_mode_unknown");
  }
  const entries = data.detail?.unlimited_list;
  const aliases = Array.isArray(entries) ? entries.flatMap(entry =>
    Array.isArray(entry?.alias_list) ? entry.alias_list.filter(alias => typeof alias === "string") : []) : [];
  return { billing_mode: data.mode, unlimited_models: aliases };
}

async function main() {
  const o = { out: null, prompt: null, refs: [], aspect: null, model: LOVART_DEFAULT_MODEL,
              mode: null, lv: null, timeout: 300, json: JSON_MODE, queryMode: false, requireFree: false };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    switch (a[i]) {
      case "-h": case "--help": printHelp(); process.exit(0);
      case "--out": o.out = a[++i]; break;
      case "--prompt": o.prompt = a[++i]; break;
      case "--prompt-file": o.prompt = await readFile(a[++i], "utf-8"); break;
      case "--ref": o.refs.push(a[++i]); break;
      case "--aspect": o.aspect = a[++i]; break;
      case "--model": o.model = a[++i]; break;
      case "--mode": o.mode = a[++i]; break;
      case "--lv": o.lv = a[++i]; break;
      case "--timeout": o.timeout = Number(a[++i]); break;
      case "--query-mode": o.queryMode = true; break;
      case "--require-free": o.requireFree = true; break;
      case "--json": o.json = true; JSON_MODE = true; break;
      default: fail("unknown flag: " + (a[i]), "invalid_args");
    }
  }
  if (!o.queryMode) {
    if (!o.out) fail("--out is required", "invalid_args");
    o.out = path.resolve(o.out);
    if (!o.prompt || !o.prompt.trim()) fail("--prompt (or --prompt-file) is required", "invalid_args");
  }

  let lv;
  try { lv = resolveLv(o.lv); }
  catch (error) { fail(error.message, "not_configured"); }
  if (!lv) fail("Lovart client is missing. See SETUP.md for supported client and credential setup.", "not_configured");

  const start = Date.now();
  billing = { auth: lv.auth, billing_mode: null };
  if (lv.auth === "shipped-client" && (!lv.env.LOVART_ACCESS_KEY?.trim() || !lv.env.LOVART_SECRET_KEY?.trim())) {
    fail("Lovart is missing credentials. See SETUP.md for credential setup.", "not_configured");
  }
  const mode = await queryBilling(lv);
  billing.billing_mode = mode.billing_mode;
  if (o.queryMode) {
    console.log(JSON.stringify({ status: "ok", ...billing, unlimited_models: mode.unlimited_models }));
    return;
  }
  if (mode.billing_mode !== "unlimited" || !mode.unlimited_models.includes(o.model)) {
    process.stderr.write("本张会扣 Lovart 积分 (this image would spend Lovart credits).\n");
    if (o.requireFree) fail("Lovart generation requires unlimited mode and a whitelisted model.", "would_spend_credits");
  }

  // 1) 参考图先传 CDN（upload 按内容嗅探，扩展名不符也吃）
  const attachments = [];
  for (const ref of o.refs) {
    if (!existsSync(ref)) fail("ref not found: " + (ref), "invalid_args");
    const r = await runProcess(lv.cmd, [...lv.args, "upload", "--file", ref], 120, lv.env);
    const j = lastJson(r.out);
    if (r.code !== 0 || !j || !j.url)
      fail("upload failed for " + (path.basename(ref)) + ": " + ((j && j.message) || r.err.trim().slice(0, 200)));
    attachments.push(j.url);
  }

  // 2) 比例只能写进提示词——Lovart CLI 没有 aspect/ratio 参数
  let prompt = o.prompt.trim();
  if (o.aspect) {
    const [w, h] = o.aspect.split(":").map(Number);
    const orient = w && h ? (h > w ? "vertical" : w > h ? "horizontal" : "square") : "";
    prompt += (" " + orient + " " + o.aspect + ".").replace(/\s+/g, " ");
  }

  // 3) 每次都开新 thread（不传 --thread-id）：同 thread 并发提交会 409，不同 thread 才能并行
  const tmp = path.join(path.dirname(path.resolve(o.out)), ".lovart-" + (process.pid) + "-" + (Date.now()));
  await mkdir(tmp, { recursive: true });
  await markRunDir(tmp);
  const args = ["chat", "--prompt", prompt, "--json", "--download", "--output-dir", tmp];
  if (attachments.length) args.push("--attachments", ...attachments);
  if (o.model) args.push("--prefer-models", JSON.stringify({ IMAGE: [o.model] }));
  if (o.mode) args.push("--mode", o.mode);

  const r = await runProcess(lv.cmd, [...lv.args, ...args], o.timeout, lv.env);
  if (r.killed) { await rm(tmp, { recursive: true, force: true }).catch(() => {});
                  fail("timed out after " + (o.timeout) + "s", "timeout"); }
  const j = lastJson(r.out);
  if (r.code !== 0 || !j) { await rm(tmp, { recursive: true, force: true }).catch(() => {});
                            fail(r.err.trim().slice(0, 300) || "no JSON from lv"); }

  // agent 可能只回文字：内容审核拒绝 / 超时 / 没调生成工具。CLI 会标出来，别当成功。
  if (j.generation_succeeded !== true) {
    await rm(tmp, { recursive: true, force: true }).catch(() => {});
    fail("no image produced (" + (String(j.generation_note || j.final_status || "agent returned text only").slice(0, 200)) + ")", "no_image");
  }
  const got = (j.downloaded || []).find((d) => d.type === "image" && d.local_path);
  if (!got) { await rm(tmp, { recursive: true, force: true }).catch(() => {});
              fail("succeeded but no image artifact was downloaded", "no_image"); }

  await mkdir(path.dirname(path.resolve(o.out)), { recursive: true });
  // 模型可能交 JPG / WebP：统一转成真正的 PNG
  const conv = await runProcess(PY, [IMGTOOL, "png", path.resolve(got.local_path), o.out], 60);
  await rm(tmp, { recursive: true, force: true });
  if (conv.code !== 0) fail("could not convert the Lovart artifact to PNG: " + (conv.err.trim().slice(0, 200)));

  const s = await stat(o.out);
  const result = { status: "ok", provider: "lovart", path: o.out, bytes: s.size,
                   ...billing, model: o.model, aspect: o.aspect, thread_id: j.thread_id,
                   elapsed_seconds: Math.round((Date.now() - start) / 1000) };
  if (o.json) process.stdout.write(JSON.stringify(result) + "\n");
  else process.stdout.write("OK lovart " + (o.out) + "\n");
  process.exit(0);
}

if (isInvokedDirectly(import.meta.url)) main().catch((e) => fail(String(e && e.message || e)));
