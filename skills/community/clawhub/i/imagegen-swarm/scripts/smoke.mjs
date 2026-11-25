#!/usr/bin/env node
import { randomUUID } from "node:crypto";
import { writeFileSync } from "node:fs";
import { mkdir, mkdtemp, open, readFile, rename, rm, writeFile } from "node:fs/promises";
import { homedir, tmpdir } from "node:os";
import path from "node:path";
import { isInvokedDirectly } from "./direct.mjs";
import { LOVART_DEFAULT_MODEL } from "./lovart.mjs";
import {
  ENGINES, PY, SCRIPT_DIR, SMOKE_CACHE, lastJson, probeEngine, readSmokeCache, run, turnedOff,
} from "./readiness.mjs";
import { childEnv } from "./scoped-env.mjs";

const DEFAULT_TIMEOUT_SECONDS = 300;
const PROMPT = "a small red circle centered on a plain white background, flat icon";
const HELP = "node smoke.mjs [--engines codex,grok,gemini,jimeng,muse,lovart,api] [--allow-credits] [--allow-paid] [--out <dir>] [--keep] [--timeout <seconds>] [--json] [--require <engine-list>]";

function parse(args) {
  const options = { engines: ENGINES, require: [], out: null, timeout: DEFAULT_TIMEOUT_SECONDS };
  const flags = { "--allow-credits": "allowCredits", "--allow-paid": "allowPaid", "--keep": "keep", "--json": "json" };
  for (let i = 0; i < args.length; i++) {
    const flag = args[i];
    if (Object.hasOwn(flags, flag)) { options[flags[flag]] = true; continue; }
    if (!["--engines", "--require", "--out", "--timeout"].includes(flag)) throw new Error("Unknown option: " + flag);
    const value = args[++i];
    if (!value || value.startsWith("--")) throw new Error(flag + " needs a value.");
    if (flag === "--out") { options.out = path.resolve(value); continue; }
    if (flag === "--timeout") {
      options.timeout = Number(value);
      if (!Number.isFinite(options.timeout) || options.timeout <= 0 || options.timeout > 2147483) {
        throw new Error("--timeout must be positive seconds within the Node timer range.");
      }
      continue;
    }
    const engines = [...new Set(value.split(","))];
    if (engines.some(engine => !ENGINES.includes(engine))) throw new Error(flag + " contains an unknown engine.");
    options[flag.slice(2)] = engines;
  }
  if (options.require.some(engine => !options.engines.includes(engine))) {
    throw new Error("--require must name engines selected for this run.");
  }
  return options;
}

function redact(message, keyEnv) {
  let text = String(message ?? "");
  for (const [key, value] of Object.entries(process.env)) {
    if (value && (key === keyEnv || /key|secret|token|password|cookie|credential/i.test(key))) {
      text = text.replaceAll(value, "[redacted]");
    }
  }
  return text.replaceAll(homedir(), "~")
    .replace(/\b(?:agy conversation|(?:conversation|session)[ _-]?id)\b["\s:=]+[^\s,)"}]+/gi, "conversation [redacted]")
    .replace(/\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b/gi, "[redacted]")
    .replace(/\bBearer\s+[^\s,"]+/gi, "Bearer [redacted]")
    .replace(/(["']?[\w-]*(?:key|token|cookie|secret|authorization|password)["']?\s*[:=]\s*)("[^"]*"|'[^']*'|[^\s,;}]+)/gi, "$1[redacted]")
    .replace(/\b(?:sk-|AIza)[\w-]{10,}/g, "[redacted]")
    .replace(/https?:\/\/[^\s"']+/gi, "[URL]")
    .replace(/\s+/g, " ").trim().slice(0, 300);
}

async function verifyPng(file, fingerprints, env, signal) {
  const header = Buffer.alloc(8);
  const handle = await open(file, "r");
  try { await handle.read(header); } finally { await handle.close(); }
  if (header.toString("hex") !== "89504e470d0a1a0a") throw new Error("Output is not a PNG.");
  const imgtool = path.join(SCRIPT_DIR, "imgtool.py");
  const size = await run(PY, [imgtool, "size", file], { env, signal });
  const dimensions = lastJson(size.stdout);
  if (size.code !== 0 || !dimensions) throw new Error("PNG dimensions could not be read.");
  if (!(dimensions.width >= 256 && dimensions.height >= 256)) throw new Error("PNG must be at least 256×256.");
  const hash = await run(PY, [imgtool, "fp", file], { env, signal });
  const fingerprint = lastJson(hash.stdout)?.fp?.[0];
  if (hash.code !== 0 || !fingerprint) throw new Error("PNG could not be decoded for fingerprinting.");
  if (fingerprints.has(fingerprint)) throw new Error("PNG matches an earlier output in this run.");
  fingerprints.add(fingerprint);
}

const skip = reason => ({ result: "SKIP", reason });
const failure = (error_kind, reason) => ({ result: "FAIL", error_kind, reason });

async function runEngine(engine, options, scripts, artifacts, fingerprints, env, signal) {
  const optInReason = engine === "api" && !options.allowPaid
    ? "Pay-per-image API. Pass --allow-paid to test using the configured budget."
    : engine === "jimeng" && !options.allowCredits ? "Dreamina uses credits. Pass --allow-credits to test." : null;
  if (optInReason && !turnedOff(engine, env)) return skip(optInReason);
  const probe = await probeEngine(engine, { scripts, env, signal });
  if (!probe.loggedIn) return skip(probe.reason);
  if (optInReason) return skip(optInReason);
  if (engine === "lovart" && !probe.free && !options.allowCredits) {
    return skip(probe.billingMode === "fast"
      ? "Lovart is in fast mode and would spend credits. --allow-credits opts in; smoke never changes billing mode."
      : "Default Lovart model is outside the unlimited whitelist. Pass --allow-credits to opt in.");
  }

  const file = path.join(artifacts, engine + ".png");
  const args = ["--prompt", PROMPT, "--out", file, engine === "grok" ? "--ratio" : "--aspect", "1:1", "--json"];
  const seconds = options.timeout;
  let script = engine + "-image.mjs", bin = process.execPath;
  if (engine === "codex") {
    args.push("--retries", "0");
    // The bare command is resolved on PATH by codex-image. Its --codex flag requires a file.
    if (probe.codex !== "codex") args.push("--codex", probe.codex);
  }
  if (engine === "gemini") args.push("--agy", probe.agy);
  if (engine === "muse") {
    script = "muse-image.py";
    bin = PY;
  }
  if (engine === "lovart") {
    script = "lovart.mjs";
    args.push("--model", LOVART_DEFAULT_MODEL);
    if (!options.allowCredits) args.push("--require-free");
  }
  args.push("--timeout", String(engine === "lovart" ? Math.ceil(seconds) : Math.max(1, Math.round(seconds * 1000))));
  const engineEnv = probe.keyEnv && process.env[probe.keyEnv]
    ? { ...env, [probe.keyEnv]: process.env[probe.keyEnv] } : env;
  const execution = await run(bin, [path.join(scripts, script), ...args], { timeout: seconds * 1000, env: engineEnv, signal });
  const exit = execution.code === null ? {} : { exit_code: execution.code };
  if (execution.timedOut) return failure("timeout", "Generation timed out after " + seconds + " seconds.");
  const reply = lastJson(execution.stdout);
  const kind = typeof reply?.error_kind === "string" && /^[a-z_][a-z0-9_-]{0,79}$/i.test(reply.error_kind)
    ? reply.error_kind : null;
  if (engine === "gemini" && kind === "quota_exhausted") {
    return { ...skip("额度: " + redact(reply.reason ?? reply.error ?? "Antigravity image quota exhausted.")), error_kind: kind, ...exit };
  }
  if (engine === "codex" && kind === "image_gen_unavailable") {
    return { ...skip("This Codex account lacks image_gen. Sign in with an account that includes the image tool."), ...exit };
  }
  if (engine === "lovart" && kind === "would_spend_credits" && !options.allowCredits) {
    return { ...skip("Lovart billing changed before generation. Verify unlimited mode and the whitelist before retrying."), ...exit };
  }
  if (execution.code !== 0 || reply?.status !== "ok" || reply?.error_kind) {
    const detail = reply?.error ?? reply?.reason ?? execution.stderr.trim();
    return { ...failure(kind || "generation_failed", redact(detail, probe.keyEnv) || "Engine exited without a successful JSON result."), ...exit };
  }
  try {
    await verifyPng(file, fingerprints, env, signal);
  } catch (error) {
    return { ...failure("invalid_png", redact(error.message)), ...exit };
  }
  const location = probe.remoteDir ? " remote_dir=" + redact(probe.remoteDir) : "";
  return { result: "PASS", reason: "Unique PNG of at least 256×256." + location, ...exit,
    ...(options.keep && { image: file.replace(homedir(), "~") }) };
}

async function saveCache(file, rows) {
  await mkdir(path.dirname(file), { recursive: true });
  const results = await readSmokeCache(file);
  for (const row of rows) {
    const { error_kind, image, exit_code, ...entry } = row;
    if (row.result === "FAIL" && error_kind) entry.reason = "Generation or image validation failed. See the smoke log.";
    results[row.engine] = entry;
  }
  const temp = file + "." + randomUUID() + ".tmp";
  try {
    await writeFile(temp, JSON.stringify({ engines: results }, null, 2) + "\n", { mode: 0o600, flag: "wx" });
    await rename(temp, file);
  } finally {
    await rm(temp, { force: true });
  }
}

export async function smokeMain(args = process.argv.slice(2)) {
  if (args.includes("--help") || args.includes("-h")) { console.log(HELP); return 0; }
  const options = parse(args);
  const fixture = process.env.IMAGE_GEN_SMOKE_SCRIPTS_DIR;
  const scripts = fixture ? path.resolve(fixture) : SCRIPT_DIR;
  // Preserve test fixture controls in the test lane. Production only passes the skill's scoped environment.
  const env = fixture ? { ...process.env } : childEnv();
  const skill = await readFile(path.join(SCRIPT_DIR, "..", "SKILL.md"), "utf8");
  const version = skill.match(/^version:\s*(\S+)$/m)?.[1];
  const out = options.out || tmpdir();
  if (options.out) await mkdir(out, { recursive: true });
  const directory = await mkdtemp(path.join(out, "imagegen-smoke-"));
  const artifacts = path.join(directory, "images");
  await mkdir(artifacts);
  const fingerprints = new Set(), rows = [];
  const interrupted = new AbortController();
  const interrupt = signal => interrupted.abort(signal);
  const onInt = () => interrupt("SIGINT");
  const onTerm = () => interrupt("SIGTERM");
  process.on("SIGINT", onInt);
  process.on("SIGTERM", onTerm);
  const progress = options.json ? console.error : console.log;
  let geminiVersion = "unavailable";
  function formatRow(row) {
    return row.engine.padEnd(9) + row.result.padEnd(8) + (row.elapsed_ms / 1000).toFixed(1).padEnd(9)
      + (row.error_kind ? row.error_kind + ": " : "") + row.reason
      + (row.exit_code === undefined ? "" : " | engine exit " + row.exit_code)
      + (row.image ? " | " + row.image : "");
  }
  try {
    for (const engine of options.engines) {
      const start = Date.now();
      let verdict;
      if (interrupted.signal.aborted) {
        verdict = skip("Not started due to " + interrupted.signal.reason + ".");
      } else {
        progress("START " + engine);
        const controller = new AbortController();
        const signal = AbortSignal.any([interrupted.signal, controller.signal]);
        const timer = setTimeout(() => controller.abort(), options.timeout * 1000);
        try {
          if (engine === "gemini" && !turnedOff(engine, env)) {
            const agy = env.AGY_BIN || path.join(homedir(), ".local", "bin", "agy");
            const versionResult = await run(agy, ["--version"], { env, signal });
            geminiVersion = versionResult.stdout.trim().match(/^v?\d+\.\d+\.\d+(?:[-+][\w.-]+)?$/)?.[0] || "unavailable";
          }
          verdict = await runEngine(engine, options, scripts, artifacts, fingerprints, env, signal);
        } catch (error) {
          verdict = failure("smoke_error", redact(error.message));
        } finally {
          clearTimeout(timer);
        }
        if (interrupted.signal.aborted) {
          verdict = failure("interrupted", "Interrupted by " + interrupted.signal.reason + ".");
        } else if (controller.signal.aborted) {
          verdict = failure("timeout", "Engine exceeded " + options.timeout + " seconds.");
        }
      }
      const row = { time: new Date().toISOString(), engine, ...verdict, elapsed_ms: Date.now() - start, version };
      rows.push(row);
      progress(formatRow(row));
      if (options.json) console.log(JSON.stringify(row));
      if (row.result === "FAIL") {
        await writeFile(path.join(directory, engine + ".log"), row.error_kind + ": " + row.reason + "\n", { mode: 0o600 });
      }
    }
  } finally {
    const table = ["ENGINE   RESULT  SECONDS  REASON", ...rows.map(formatRow)];
    if (options.engines.includes("gemini")) {
      table.push("agy version: " + geminiVersion, "Remaining Gemini image quota: unavailable (no supported non-interactive usage query configured).");
    }
    const output = table.join("\n") + "\n";
    if (!options.json) process.stdout.write(output);
    writeFileSync(path.join(directory, "SMOKE_TABLE.txt"), output, { mode: 0o600 });
    try {
      await saveCache(fixture ? path.join(directory, "smoke-last.json") : SMOKE_CACHE, rows);
      if (!options.keep) await rm(artifacts, { recursive: true, force: true });
    } finally {
      process.removeListener("SIGINT", onInt);
      process.removeListener("SIGTERM", onTerm);
    }
  }
  if (interrupted.signal.aborted) return interrupted.signal.reason === "SIGINT" ? 130 : 143;

  if (options.keep || rows.some(row => row.result === "FAIL")) {
    console.error("Smoke output: " + directory.replace(homedir(), "~"));
  }
  return rows.some(row => row.result === "FAIL" || (row.result === "SKIP" && options.require.includes(row.engine))) ? 1 : 0;
}

if (isInvokedDirectly(import.meta.url)) {
  smokeMain().then(code => { process.exitCode = code; }).catch(error => {
    console.error(redact(error.message));
    process.exitCode = 1;
  });
}
