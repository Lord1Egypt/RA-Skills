#!/usr/bin/env node
// jimeng.mjs — thin wrapper around the Dreamina CLI binary named dreamina.
// Submits a media-generation subcommand (image or video), polls query_result
// until the task finishes, and downloads the result locally. Other Dreamina
// commands (login, account, credit transfer, and anything outside the list
// below) are rejected. Image and video share the submit_id / gen_status /
// query_result contract.
//
// Auth: uses the existing dreamina login session (Douyin OAuth). No API key.
// Credits: real submits consume account credits. Check with: dreamina user_credit
//
// Usage:
//   node jimeng.mjs <subcommand> [--out <dir>] [--poll <sec>] [--interval <sec>]
//                   [--dreamina <path>] [--json] [passthrough dreamina flags...]
// Any flag the wrapper does not recognize is forwarded verbatim to the dreamina
// subcommand, e.g.:
//   node jimeng.mjs text2image --out imgs --prompt="a cat portrait" --ratio=1:1 --resolution_type=2k
//   node jimeng.mjs text2video --out vids --prompt="a drone shot over dunes" --poll 600
//
// Exit: 0 on success, 1 on failure/timeout, 2 on bad args.

import { spawn } from "node:child_process";
import { readdir, mkdir, stat } from "node:fs/promises";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { STDIO_DISCARD, STDIO_PIPE } from "./stdio-modes.mjs";

const GEN_SUBCOMMANDS = new Set([
  "text2image", "image2image", "image_upscale",
  "text2video", "image2video", "frames2video", "multiframe2video", "multimodal2video",
]);
// Flags the image and video scripts pass through. Anything else is out of scope.
const MEDIA_FLAG = /^(--prompt|--ratio|--resolution_type|--generate_num|--images|--image|--video_resolution|--model_version)(=|$)/;

function parseArgs(argv) {
  const o = { sub: "", out: null, pollSec: 300, intervalSec: 4, dreamina: null, json: false, passthrough: [] };
  if (argv.length && !argv[0].startsWith("-")) o.sub = argv.shift();
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    switch (a) {
      case "--out": o.out = argv[++i]; break;
      case "--poll": o.pollSec = Number(argv[++i]); break;
      case "--interval": o.intervalSec = Number(argv[++i]); break;
      case "--dreamina": o.dreamina = argv[++i]; break;
      case "--json": o.json = true; break;
      case "-h": case "--help": printHelp(); process.exit(0);
      default:
        if (!MEDIA_FLAG.test(a)) die(2, "flag is outside image generation scope: " + (a) + ". Allowed flags are prompt, ratio, resolution, images, and model.");
        o.passthrough.push(a);
        break;
    }
  }
  if (!o.sub) die(2, "missing <subcommand> (e.g. text2image, image2video)");
  if (!GEN_SUBCOMMANDS.has(o.sub)) die(2, "'" + (o.sub) + "' is outside image generation scope. Allowed: " + ([...GEN_SUBCOMMANDS].join(", ")));
  o.out = o.out ? path.resolve(o.out) : path.resolve(process.cwd(), "jimeng-out-" + (o.sub));
  return o;
}

function printHelp() {
  process.stdout.write("jimeng.mjs — Dreamina generator runner\n\n" +
    "node jimeng.mjs <subcommand> [--out dir] [--poll sec] [--interval sec] [--dreamina path] [--json] [dreamina flags...]\n" +
    "Subcommands: " + ([...GEN_SUBCOMMANDS].join(", ")) + "\n");
}

let JSON_MODE = false;
function warn(m) { process.stderr.write("[jimeng] " + (m) + "\n"); }
function die(code, m) {
  if (JSON_MODE) process.stdout.write(JSON.stringify({ status: "error", error: m }) + "\n");
  else process.stderr.write("Error: " + (m) + "\n");
  process.exit(code);
}

function resolveDreamina(explicit) {
  if (explicit) { if (!existsSync(explicit)) die(2, "--dreamina not found: " + (explicit)); return explicit; }
  const exe = process.platform === "win32" ? "dreamina.exe" : "dreamina";
  const candidates = [];
  if (process.env.DREAMINA_INSTALL_DIR) candidates.push(path.join(process.env.DREAMINA_INSTALL_DIR, exe));
  candidates.push(path.join(homedir(), "bin", exe));           // installer default on Windows
  candidates.push(path.join(homedir(), ".local", "bin", exe)); // installer default on macOS/Linux
  for (const c of candidates) if (existsSync(c)) return c;
  return "dreamina"; // fall back to PATH (works after reopening a terminal post-install)
}

function runProcess(bin, args) {
  return new Promise((resolve) => {
    let stdout = "", stderr = "";
    const child = spawn(bin, args, { stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE], shell: false });
    child.on("error", (e) => resolve({ code: -1, stdout, stderr: stderr + String(e) }));
    child.stdout.on("data", (c) => { stdout += c.toString(); });
    child.stderr.on("data", (c) => { stderr += c.toString(); });
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

// Extract the last balanced JSON object from mixed CLI stdout.
function extractJson(text) {
  const end = text.lastIndexOf("}");
  if (end < 0) return null;
  let depth = 0, start = -1;
  for (let i = end; i >= 0; i--) {
    const ch = text[i];
    if (ch === "}") depth++;
    else if (ch === "{") { depth--; if (depth === 0) { start = i; break; } }
  }
  if (start < 0) return null;
  try { return JSON.parse(text.slice(start, end + 1)); } catch { return null; }
}

// Recursively find the first value for any of the given keys.
function findKey(obj, keys) {
  if (obj == null || typeof obj !== "object") return undefined;
  for (const k of keys) if (k in obj && obj[k] != null) return obj[k];
  for (const v of Object.values(obj)) {
    const r = findKey(v, keys);
    if (r !== undefined) return r;
  }
  return undefined;
}

async function listFiles(dir) {
  try { return new Set(await readdir(dir)); } catch { return new Set(); }
}

async function main() {
  const o = parseArgs(process.argv.slice(2));
  JSON_MODE = o.json;
  const dreamina = resolveDreamina(o.dreamina);
  await mkdir(o.out, { recursive: true });

  // 1) Submit.
  warn("submitting: " + (o.sub) + " " + (o.passthrough.join(" ")) + "  (consumes credits)");
  const submit = await runProcess(dreamina, [o.sub, ...o.passthrough]);
  if (submit.code === -1) die(1, "could not launch dreamina: " + (submit.stderr.slice(0, 300)));
  const sj = extractJson(submit.stdout) || {};
  let submitId = findKey(sj, ["submit_id", "submitId"]);
  let genStatus = findKey(sj, ["gen_status", "genStatus", "status"]);
  if (!submitId) {
    // Some commands may error out with a message rather than JSON.
    die(1, "no submit_id in response (gen_status=" + (genStatus ?? "?") + "). Raw output:\n" + ((submit.stdout + submit.stderr).slice(0, 600)));
  }
  if (genStatus === "fail") die(1, "submit failed: " + (findKey(sj, ["fail_reason", "failReason"]) ?? "unknown") + " (submit_id=" + (submitId) + ")");
  warn("submitted. submit_id=" + (submitId) + " gen_status=" + (genStatus ?? "querying"));

  // 2) Poll query_result, downloading into --out once the task succeeds.
  const before = await listFiles(o.out);
  const deadline = Date.now() + o.pollSec * 1000;
  let lastStatus = genStatus;
  while (Date.now() < deadline) {
    const q = await runProcess(dreamina, ["query_result", "--submit_id=" + (submitId), "--download_dir=" + (o.out)]);
    const qj = extractJson(q.stdout) || {};
    const st = findKey(qj, ["gen_status", "genStatus", "status"]) ?? lastStatus;
    lastStatus = st;
    if (st === "success") {
      const after = await listFiles(o.out);
      const added = [...after].filter((f) => !before.has(f));
      const files = [];
      for (const f of added) { const p = path.join(o.out, f); try { files.push({ path: p, bytes: (await stat(p)).size }); } catch {} }
      const result = { status: "ok", provider: "jimeng", subcommand: o.sub, submit_id: submitId, out_dir: o.out, files };
      if (o.json) process.stdout.write(JSON.stringify(result) + "\n");
      else {
        process.stdout.write("OK  jimeng/" + (o.sub) + "  submit_id=" + (submitId) + "\n");
        if (files.length) for (const f of files) process.stdout.write("    " + (f.path) + "  (" + (f.bytes) + " bytes)\n");
        else process.stdout.write("    (task success; media downloaded into " + (o.out) + " — check that dir)\n");
      }
      process.exit(0);
    }
    if (st === "fail") die(1, "generation failed: " + (findKey(qj, ["fail_reason", "failReason"]) ?? "unknown") + " (submit_id=" + (submitId) + ")");
    warn("  ..." + (st ?? "querying") + " (submit_id=" + (submitId) + ")");
    await delay(o.intervalSec * 1000);
  }
  die(1, "timed out after " + (o.pollSec) + "s (last status=" + (lastStatus) + "). Task still running — resume later with:\n  dreamina query_result --submit_id=" + (submitId) + " --download_dir=" + (o.out));
}

main().catch((e) => die(1, String(e?.stack || e)));
