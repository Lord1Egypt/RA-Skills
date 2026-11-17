#!/usr/bin/env node
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { readdir, stat } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import process from "node:process";
import { childEnv } from "./scoped-env.mjs";
import { STDIO_DISCARD, STDIO_PIPE } from "./stdio-modes.mjs";

const ok = (m) => "  ✅ " + (m);
const no = (m) => "  ❌ " + (m);
const line = (m) => process.stdout.write(m + "\n");

function turnedOff(engine) {
  const dirs = process.env.IMAGE_GEN_ENGINE_OFF
    ? [process.env.IMAGE_GEN_ENGINE_OFF]
    : [path.join(homedir(), ".config", "imagegen-swarm", "engine-off"), path.join(homedir(), ".config", "image-gen", "engine-off")];
  return dirs.map((dir) => path.join(dir, engine)).find((file) => existsSync(file)) || null;
}

function probe(bin, args, env) {
  return new Promise((res) => {
    let out = "";
    const c = spawn(bin, args, { stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE], env: childEnv(env), shell: process.platform === "win32" && !path.isAbsolute(bin) });
    c.on("error", () => res({ code: -1, out }));
    c.stdout.on("data", (d) => (out += d.toString()));
    c.stderr.on("data", (d) => (out += d.toString()));
    c.on("close", (code) => res({ code, out }));
  });
}

async function resolveCodex() {
  if (process.env.CODEX_BIN && existsSync(process.env.CODEX_BIN)) return process.env.CODEX_BIN;
  const onPath = await new Promise((r) => {
    const c = spawn("codex", ["--version"], { stdio: STDIO_DISCARD, shell: process.platform === "win32" });
    c.on("error", () => r(false));
    c.on("close", (code) => r(code === 0));
  });
  if (onPath) return "codex";
  for (const exe of ["/Applications/Codex.app/Contents/Resources/codex", path.join(homedir(), "Applications", "Codex.app", "Contents", "Resources", "codex")]) {
    if (existsSync(exe)) return exe;
  }
  const binDir = path.join(homedir(), "AppData", "Local", "OpenAI", "Codex", "bin");
  if (existsSync(binDir)) {
    let best = null, m = 0;
    for (const d of await readdir(binDir).catch(() => [])) {
      const exe = path.join(binDir, d, "codex.exe");
      try { const s = await stat(exe); if (s.mtimeMs > m) { m = s.mtimeMs; best = exe; } } catch {}
    }
    if (best) return best;
  }
  return null;
}

async function main() {
  line("imagegen-swarm readiness check\n==============================");

  line("Node: " + (process.version) + "  (" + (process.platform) + "/" + (process.arch) + ")");
  line(ok("node is running this script"));
  const py = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
  const pil = await probe(py, ["-c", "import PIL; print(PIL.__version__)"]);
  const pillowReady = pil.code === 0;
  line(pillowReady ? ok("Pillow " + (pil.out.trim()) + " (" + (py) + ") — used to convert and verify images") : no("Pillow missing — run: " + (py) + " -m pip install pillow (every engine needs it)"));

  line("\n[codex engine — images]");
  const codex = await resolveCodex();
  let codexReady = false;
  if (codex) {
    const v = await probe(codex, ["--version"]);
    line(ok("codex found: " + (codex) + (v.code === 0 ? "  (" + (v.out.trim().split("\n")[0]) + ")" : "")));
    const auth = path.join(process.env.CODEX_HOME || path.join(homedir(), ".codex"), "auth.json");
    if (existsSync(auth)) { line(ok("codex login state present (auth.json)")); codexReady = true; }
    else line(no("not logged in — run: codex login"));
  } else {
    line(no("codex not found — install @openai/codex (npm i -g @openai/codex) or the Codex app, then: codex login"));
  }

  line("\n[grok engine — images + edits + video]");
  const g = await probe("grok", ["models"]);
  const grokReady = g.code === 0 && /grok-[\w.-]+/i.test(g.out);
  line(grokReady ? ok("grok models lists models — logged in") : no("grok models failed or returned no models; check Grok login/network/sandbox"));

  line("\n[gemini engine — images + edits (Antigravity agy)]");
  const agy = process.env.AGY_BIN || path.join(homedir(), ".local", "bin", "agy");
  let geminiReady = false;
  if (existsSync(agy)) {
    const m = await probe(agy, ["models"]);
    geminiReady = m.code === 0 && /gemini-[\w.-]+/i.test(m.out);
    line(geminiReady ? ok("agy models lists Gemini models — logged in (" + (agy) + ")") : no("agy models failed or listed no Gemini model; sign in to Antigravity"));
  } else {
    line(no("agy not found at " + (agy) + " — install the Antigravity CLI and sign in"));
  }

  line("\n[jimeng engine — images + edits + video (Dreamina CLI)]");
  const dreamina = [process.env.DREAMINA_INSTALL_DIR && path.join(process.env.DREAMINA_INSTALL_DIR, process.platform === "win32" ? "dreamina.exe" : "dreamina"), path.join(homedir(), "bin", process.platform === "win32" ? "dreamina.exe" : "dreamina"), path.join(homedir(), ".local", "bin", "dreamina")].filter(Boolean).find((p) => existsSync(p)) || "dreamina";
  const offFile = turnedOff("jimeng");
  let jimengReady = false;
  if (offFile) {
    line(no("turned off (" + (offFile) + "); not checked"));
  } else {
    const credit = await probe(dreamina, ["user_credit"]);
    const creditMatch = credit.out.match(/"total_credit"\s*:\s*(\d+)/);
    jimengReady = credit.code === 0 && Boolean(creditMatch);
    line(jimengReady ? ok("dreamina logged in — " + (creditMatch[1]) + " credits") : no("dreamina not installed or not logged in — install the pinned binary in SETUP.md yourself, then: dreamina login"));
  }

  line("\n[muse engine — images (Muse cloud computer)]");
  const musePy = path.join(path.dirname(new URL(import.meta.url).pathname), "muse-image.py");
  const d = await probe("python3", [musePy, "--list-chats"]);
  let report = null;
  try { report = JSON.parse(d.out.slice(d.out.indexOf("{"), d.out.lastIndexOf("}") + 1)); } catch {}
  const museReady = d.code === 0 && Array.isArray(report?.chats);
  line(museReady ? ok("muse-image.py --list-chats lists side chats — logged in") : no("not logged in to Muse; run: python3 " + (musePy) + " --login (needs: pip install playwright && playwright install chromium)"));

  line("\n[lovart engine — images]");
  const { readLovartEnv, LOVART_AGENT } = await import("./lovart.mjs");
  const lv = [process.env.LOVART_LV, path.join(homedir(), "tools", "lovart-skill", "lv")]
    .filter(Boolean).find((p) => existsSync(p));
  let lovartCmd = null, lovartArgs = null, lovartEnv = null;
  if (lv) {
    lovartCmd = lv; lovartArgs = ["query-mode"];
    line(ok("lv wrapper found: " + (lv)));
  } else if (existsSync(LOVART_AGENT)) {
    try {
      lovartEnv = readLovartEnv();
      lovartCmd = py; lovartArgs = [LOVART_AGENT, "query-mode"];
      line(ok("shipped client: " + (LOVART_AGENT)));
    } catch (error) { line(no(String(error.message || error))); }
  }
  let lovartReady = false;
  if (lovartCmd && lovartArgs) {
    const q = await probe(lovartCmd, lovartArgs, lovartEnv);
    let mode = null, unlimited = null;
    try {
      const j = JSON.parse(q.out.slice(q.out.indexOf("{"), q.out.lastIndexOf("}") + 1));
      mode = j.mode; unlimited = j.detail && j.detail.unlimited;
    } catch {}
    if (mode) {
      line(ok("key valid — billing mode " + (mode) + " (" + (unlimited ? "free, may queue" : "spends credits, no queue") + ")"));
      lovartReady = true;
    } else {
      line(no("key invalid or unreachable — open the Lovart avatar menu, OpenClaw for Lovart, " +
              "copy the API key into the file $HOME/.lovart/env (see SETUP.md). That file is read as text."));
    }
  } else if (!lv && !existsSync(LOVART_AGENT)) {
    line(no("Lovart client missing. See SETUP.md for the file $HOME/.lovart/env. Do not clone or run a remote installer."));
  }

  line("\n[api line — pay per image, last resort]");
  const { loadApiConfig, readKey, readLedger, CONFIG_FILE } = await import("./api-image.mjs");
  const api = loadApiConfig();
  let apiReady = false;
  if (!api) {
    line("  ➖ off — no " + (CONFIG_FILE) + " (optional; see SETUP.md)");
  } else {
    // 只调免费的模型列表接口验证 key，不出图、不花钱
    const key = readKey(api);
    const url = api.provider === "openai" ? (api.base) + "/v1/models" : (api.base) + "/v1beta/models";
    const headers = api.provider === "openai" ? { Authorization: "Bearer " + (key) } : { "x-goog-api-key": key };
    const res = await fetch(url, { headers, signal: AbortSignal.timeout(20000) });
    apiReady = res.ok;
    const spent = readLedger();
    line(apiReady ? ok((api.provider) + " key works (" + (api.model) + ")") : no((api.provider) + " key rejected: HTTP " + (res.status) + " " + ((await res.text()).slice(0, 200))));
    line("  💵 " + (spent.month) + ": " + (spent.images) + " images, about $" + (spent.usd) + " of $" + (api.budgetMonth) + "; per batch up to $" + (api.budgetBatch) + ", about $" + (api.price) + " each");
  }

  line("\n==========================");
  line("codex  (images):        " + (codexReady ? "READY ✅" : "NOT READY ❌"));
  line("grok   (images+video):  " + (grokReady ? "READY ✅" : "NOT READY ❌"));
  line("gemini (images+edits):  " + (geminiReady ? "READY ✅" : "NOT READY ❌"));
  line("jimeng (images+video):  " + (jimengReady ? "READY ✅" : "NOT READY ❌"));
  line("muse   (images):        " + (museReady ? "READY ✅" : "NOT READY ❌"));
  line("lovart (images):        " + (lovartReady ? "READY ✅" : "NOT READY ❌"));
  line("api    (paid, last):    " + (api ? (apiReady ? "READY ✅" : "NOT READY ❌") : "OFF ➖"));
  if (!pillowReady) { line("\nInstall Pillow first — every engine uses it."); process.exit(1); }
  if (!codexReady && !grokReady && !geminiReady && !jimengReady && !museReady && !lovartReady) { line("\nNo engine ready yet — see SETUP.md."); process.exit(1); }
  line("\nAt least one engine is ready. See SETUP.md for anything marked ❌.");
}

main().catch((e) => { line(no(String(e?.stack || e))); process.exit(1); });
