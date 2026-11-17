#!/usr/bin/env node
// nimble-decision — call an Ollama decision model (/v1/systemone) and return probabilities.
// Config lives in one file (config.json or $NIMBLE_CONFIG). Model name is NOT hardcoded here.
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync, statSync, renameSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const HERE = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = process.env.NIMBLE_CONFIG
  ? process.env.NIMBLE_CONFIG.replace(/^~(?=\/)/, process.env.HOME || "")
  : join(HERE, "config.json");
const DEFAULT_TIMEOUT = 180000;
const DEFAULT_LOG = "./logs/calls.jsonl";

const HELP = [
  "nimble-decision — classify / route / score text with an Ollama decision model",
  "",
  "Usage:",
  "  node nimble.mjs \"{\\\"state\\\":\\\"...\\\",\\\"questions\\\":{...}}\"",
  "  cat payload.json | node nimble.mjs",
  "  node nimble.mjs --state-file input.txt \"{\\\"questions\\\":{...}}\"",
  "",
  "Config (single place to change the model):",
  "  node nimble.mjs --set-model nimble-v3:9b    # auto-runs the eval when the model changes",
  "  node nimble.mjs --check                     # config + host + model + smoke test",
  "  node nimble.mjs --eval                      # run the 12-case accuracy suite now",
  "",
  "Options:",
  "  --agent <id>          agent id recorded in the call log (default: $NIMBLE_AGENT_ID or config.agentId)",
  "  --model <name>        one-off model override (does NOT persist)",
  "  --state <text>        state text instead of putting it in the JSON payload",
  "  --state-file <path>   read state text from a file",
  "  --answers-only        print only the answers object",
  "  --pretty              indented JSON output",
  "  --dry                 print the request payload, do not call the API",
  "  --schema              print question-type rules",
  "  --selftest            run all three question types against the model",
  "  --logs                show recent call log entries (in the skill folder by default)",
  "  --limit <n>           rows for --logs (default 20)",
  "  --json                raw JSON for --logs",
  "  --status <ok|error>   filter --logs by status",
  "  --kind <call|eval>    filter --logs by record kind",
  "  --no-log              do not append to the call log for this invocation",
  "  --debug               timing/usage on stderr",
  "  -h, --help",
  "",
  "Exit codes: 0 ok, 1 API/network error, 2 bad input, 3 config error",
].join("\n");

const SCHEMA = [
  "Question types (all require \"instructions\"):",
  "",
  "  noul    { \"type\":\"noul\", \"instructions\":\"...\", \"criteria\":{\"true\":\"...\",\"false\":\"...\"} }",
  "          -> { \"type\":\"noul\", \"noul\": 0.98 }        // probability the answer is true",
  "",
  "  choice  { \"type\":\"choice\", \"instructions\":\"...\", \"criteria\":{\"key\":\"description\"} }",
  "          -> { \"type\":\"choice\", \"choice\":\"key\", \"probabilities\":{...}, \"confidence\":0.99 }",
  "",
  "  score   { \"type\":\"score\", \"instructions\":\"...\", \"criteria\":[\"level0\",\"level1\"] }",
  "          -> { \"type\":\"score\", \"score\":2.09, \"legend\":{...}, \"probabilities\":{...}, \"confidence\":0.32 }",
  "",
  "Rules: 2-10 score levels, ascending. choice/noul description values may be null.",
  "Aliases accepted: score \"levels\" -> criteria, choice \"options\" -> criteria.",
  "Multiple questions per request are evaluated in one call (32K token window).",
].join("\n");

function die(msg, code) {
  console.error(msg);
  process.exit(code);
}

function expandHome(p) {
  return String(p).replace(/^~(?=\/)/, process.env.HOME || "");
}

// Relative log paths are resolved inside the skill folder, so the default stays portable.
function resolveLogPath(p) {
  const v = expandHome(p);
  return v.startsWith("/") ? v : join(HERE, v);
}

function loadConfig() {
  if (!existsSync(CONFIG_PATH)) {
    die("missing config: " + CONFIG_PATH + " (copy config.json next to SKILL.md, or set NIMBLE_CONFIG)", 3);
  }
  let cfg;
  try { cfg = JSON.parse(readFileSync(CONFIG_PATH, "utf8")); }
  catch (e) { die("invalid config JSON: " + e.message, 3); }
  if (!cfg.model || typeof cfg.model !== "string") die("config.model is required in " + CONFIG_PATH, 3);
  return {
    model: cfg.model,
    baseUrl: String(cfg.baseUrl || "http://localhost:11434").replace(/\/$/, ""),
    timeoutMs: Number(cfg.timeoutMs) > 0 ? Number(cfg.timeoutMs) : DEFAULT_TIMEOUT,
    maxStateChars: Number(cfg.maxStateChars) > 0 ? Number(cfg.maxStateChars) : 24000,
    agentId: cfg.agentId || "unknown",
    logFile: cfg.logFile === undefined ? DEFAULT_LOG : String(cfg.logFile),
    logMaxBytes: Number(cfg.logMaxBytes) > 0 ? Number(cfg.logMaxBytes) : 5242880,
  };
}

function saveConfig(cfg) {
  const tmp = CONFIG_PATH + ".tmp";
  writeFileSync(tmp, JSON.stringify(cfg, null, 2) + "\n");
  renameSync(tmp, CONFIG_PATH);
}

function localIso(d = new Date()) {
  const off = -d.getTimezoneOffset();
  const p2 = (n) => String(Math.floor(Math.abs(n))).padStart(2, "0");
  const sign = off >= 0 ? "+" : "-";
  const body = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 23);
  return body + sign + p2(off / 60) + ":" + p2(off % 60);
}

// Append one call record. Never stores state or answers. Failures are silent by design.
function logCall(cfg, entry, disabled) {
  if (disabled || process.env.NIMBLE_NO_LOG === "1") return;
  if (!cfg.logFile) return;
  try {
    const p = resolveLogPath(cfg.logFile);
    mkdirSync(dirname(p), { recursive: true });
    try {
      if (statSync(p).size >= cfg.logMaxBytes) renameSync(p, p + ".1");
    } catch {}
    appendFileSync(p, JSON.stringify(entry) + "\n");
  } catch (e) {
    console.error("warning: cannot write log: " + e.message);
  }
}

function parseArgs(argv) {
  const o = { positional: [], flags: {} };
  const takesValue = ["--model", "--state", "--state-file", "--set-model", "--set-base-url", "--agent", "--limit", "--status", "--kind"];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (takesValue.includes(a)) {
      const v = argv[++i];
      if (v === undefined) die("missing value for " + a, 2);
      o.flags[a.slice(2)] = v;
    } else if (a === "-h" || a === "--help") {
      o.flags.help = true;
    } else if (a.startsWith("--")) {
      o.flags[a.slice(2)] = true;
    } else {
      o.positional.push(a);
    }
  }
  return o;
}

function normalizeQuestion(name, q) {
  if (!q || typeof q !== "object") die("question " + name + " must be an object", 2);
  const type = q.type;
  if (!["noul", "choice", "score"].includes(type)) die("question " + name + ": unknown type " + type + " (use noul|choice|score)", 2);
  if (typeof q.instructions !== "string" || !q.instructions.trim()) die("question " + name + ": instructions is required", 2);
  const out = { ...q };
  if (type === "score") {
    if (out.criteria === undefined && Array.isArray(out.levels)) { out.criteria = out.levels; delete out.levels; }
    if (!Array.isArray(out.criteria) || out.criteria.length < 2 || out.criteria.length > 10) {
      die("question " + name + ": score needs criteria = array of 2-10 level strings", 2);
    }
    out.criteria = out.criteria.map(String);
  }
  if (type === "choice") {
    if (out.criteria === undefined && out.options) {
      out.criteria = Array.isArray(out.options) ? Object.fromEntries(out.options.map((k) => [String(k), null])) : out.options;
      delete out.options;
    }
    const c = out.criteria;
    if (!c || typeof c !== "object" || Array.isArray(c) || Object.keys(c).length < 2) {
      die("question " + name + ": choice needs criteria = { optionKey: description|null } with >= 2 options", 2);
    }
  }
  if (type === "noul" && out.criteria !== undefined && (typeof out.criteria !== "object" || Array.isArray(out.criteria))) {
    die("question " + name + ": noul criteria must be { true: ..., false: ... }", 2);
  }
  return out;
}

function buildPayload(raw, opts, cfg) {
  let body;
  try { body = JSON.parse(raw); } catch (e) { die("payload is not valid JSON: " + e.message, 2); }
  if (!body || typeof body !== "object" || Array.isArray(body)) die("payload must be a JSON object", 2);
  if (opts.flags.state) body.state = opts.flags.state;
  if (body.state === undefined) die("missing state (pass it in the JSON, --state, or --state-file)", 2);
  body.state = typeof body.state === "string" ? body.state : JSON.stringify(body.state);
  if (!body.state.trim()) die("state is empty", 2);
  if (body.state.length > cfg.maxStateChars) {
    die("state is " + body.state.length + " chars, over maxStateChars=" + cfg.maxStateChars + " (32K token window)", 2);
  }
  const qs = body.questions;
  if (!qs || typeof qs !== "object" || Array.isArray(qs) || !Object.keys(qs).length) die("missing questions object", 2);
  const questions = {};
  for (const [name, q] of Object.entries(qs)) questions[name] = normalizeQuestion(name, q);
  return { model: opts.flags.model || cfg.model, ...body, questions };
}

async function post(path, payload, timeoutMs, baseUrl) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), timeoutMs);
  try {
    const res = await fetch(baseUrl + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: ac.signal,
    });
    const text = await res.text();
    return { ok: res.ok, status: res.status, text };
  } finally { clearTimeout(timer); }
}

async function getJson(path, timeoutMs, baseUrl) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), Math.min(timeoutMs, 5000));
  try {
    const res = await fetch(baseUrl + path, { signal: ac.signal });
    return { ok: res.ok, status: res.status, json: res.ok ? await res.json() : null };
  } catch { return { ok: false, status: 0, json: null }; }
  finally { clearTimeout(timer); }
}

function emit(obj, opts) {
  const out = opts.flags["answers-only"] ? obj.answers : obj;
  console.log(opts.flags.pretty ? JSON.stringify(out, null, 2) : JSON.stringify(out));
}

const LAST_EVAL = join(HERE, "tests", "last-eval.json");

function readLastEval() {
  try { return JSON.parse(readFileSync(LAST_EVAL, "utf8")); } catch { return null; }
}

function runEvalSuite(cfg) {
  const outPath = join(HERE, "tests", "results.json");
  const r = spawnSync(process.execPath, [join(HERE, "tests", "eval.mjs"), "--json", outPath], {
    encoding: "utf8",
    timeout: 600000,
  });
  if (!existsSync(outPath)) return { ok: false, error: (r.stderr || "eval produced no output").slice(0, 400) };
  let res;
  try { res = JSON.parse(readFileSync(outPath, "utf8")); } catch (e) { return { ok: false, error: "bad eval output: " + e.message }; }
  const summary = {
    model: res.model,
    at: res.at,
    accuracy: res.overall.acc,
    correct: res.overall.correct,
    total: res.overall.total,
    avgLatencyMs: res.overall.avgLatencyMs,
    perLevel: res.summary,
    misses: res.rows.filter((x) => x.correctCount < (res.reps || 1)).map((x) => x.id),
  };
  writeFileSync(LAST_EVAL, JSON.stringify(summary, null, 2) + "\n");
  logCall(cfg, {
    ts: localIso(),
    agent: cfg.agentId,
    kind: "eval",
    model: summary.model,
    status: "ok",
    accuracy: summary.accuracy,
    cases: summary.total,
  }, false);
  return { ok: true, summary };
}

function printEval(summary) {
  const pct = (x) => Math.round(x * 100) + "%";
  console.log("eval: " + summary.correct + "/" + summary.total + "  " + pct(summary.accuracy) +
    "  easy " + pct(summary.perLevel.easy.acc) +
    "  medium " + pct(summary.perLevel.medium.acc) +
    "  hard " + pct(summary.perLevel.hard.acc));
  if (summary.misses && summary.misses.length) console.log("misses: " + summary.misses.join(", "));
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const cfg = loadConfig();
  const agent = opts.flags.agent || process.env.NIMBLE_AGENT_ID || cfg.agentId;
  const noLog = Boolean(opts.flags["no-log"]);

  if (opts.flags.help) { console.log(HELP); return 0; }
  if (opts.flags.schema) { console.log(SCHEMA); return 0; }

  if (opts.flags.logs) {
    const p = resolveLogPath(cfg.logFile);
    if (!cfg.logFile) { console.log("logging is disabled (config.logFile is empty)"); return 0; }
    if (!existsSync(p)) { console.log("no log yet: " + p); return 0; }
    let entries = readFileSync(p, "utf8").split("\n").filter(Boolean).map((l) => {
      try { return JSON.parse(l); } catch { return null; }
    }).filter(Boolean);
    if (opts.flags.agent) entries = entries.filter((x) => x.agent === opts.flags.agent);
    if (opts.flags.status) entries = entries.filter((x) => x.status === opts.flags.status);
    if (opts.flags.kind) entries = entries.filter((x) => x.kind === opts.flags.kind);
    const limit = Number(opts.flags.limit) > 0 ? Number(opts.flags.limit) : 20;
    const rows = entries.slice(-limit);
    if (opts.flags.json) { console.log(JSON.stringify(rows, null, 2)); return 0; }
    const pad = (s, n) => String(s === undefined ? "-" : s).padEnd(n);
    console.log(pad("TIME", 9) + pad("AGENT", 12) + pad("KIND", 6) + pad("MODEL", 16) + pad("TYPES", 14) + pad("STATUS", 7) + "MS");
    for (const r of rows) {
      const t = (r.ts || "").slice(11, 19);
      const types = Array.isArray(r.types) ? r.types.join(",") : (r.accuracy !== undefined ? "acc " + Math.round(r.accuracy * 100) + "%" : "-");
      console.log(pad(t, 9) + pad(r.agent, 12) + pad(r.kind, 6) + pad(String(r.model).slice(0, 15), 16) + pad(types, 14) + pad(r.status, 7) + (r.durationMs !== undefined ? r.durationMs : "-"));
    }
    const errs = entries.filter((x) => x.status === "error").length;
    console.log("");
    console.log(rows.length + "/" + entries.length + " entries · " + errs + " error(s) total · " + p);
    return 0;
  }

  if (opts.flags["set-model"] || opts.flags["set-base-url"]) {
    const next = { ...cfg };
    if (opts.flags["set-base-url"]) next.baseUrl = String(opts.flags["set-base-url"]).replace(/\/$/, "");
    if (opts.flags["set-model"]) next.model = String(opts.flags["set-model"]);
    const tags = await getJson("/api/tags", cfg.timeoutMs, next.baseUrl);
    if (!tags.ok) die("cannot reach " + next.baseUrl + " (/api/tags). Is Ollama running?", 1);
    const names = (tags.json.models || []).map((m) => m.name);
    if (!names.includes(next.model)) {
      die("model " + next.model + " is not installed on " + next.baseUrl + "\ninstalled: " + names.join(", "), 2);
    }
    const changed = next.model !== cfg.model;
    saveConfig(next);
    console.log("updated " + CONFIG_PATH + "\n  model:   " + next.model + "\n  baseUrl: " + next.baseUrl);
    if (!changed) {
      const prev = readLastEval();
      if (prev && prev.model === next.model) console.log("model unchanged; last eval " + Math.round(prev.accuracy * 100) + "% (not re-run)");
      return 0;
    }
    console.log("model changed: running the accuracy suite once...");
    const r = await runEvalSuite({ ...cfg, ...next, agentId: agent });
    if (!r.ok) { console.error("eval failed: " + r.error); return 0; }
    printEval(r.summary);
    console.log("saved " + LAST_EVAL);
    return 0;
  }

  if (opts.flags.eval) {
    console.log("running the accuracy suite (" + cfg.model + ")...");
    const r = await runEvalSuite({ ...cfg, agentId: agent });
    if (!r.ok) die("eval failed: " + r.error, 1);
    printEval(r.summary);
    console.log("saved " + LAST_EVAL);
    return 0;
  }

  if (opts.flags.check) {
    const model = opts.flags.model || cfg.model;
    const lines = ["config:  " + CONFIG_PATH, "model:   " + model, "baseUrl: " + cfg.baseUrl, "log:     " + (cfg.logFile || "(disabled)")];
    const ver = await getJson("/api/version", cfg.timeoutMs, cfg.baseUrl);
    if (!ver.ok) {
      console.error(lines.concat(["host:    UNREACHABLE — start it with ollama serve"]).join("\n"));
      return 1;
    }
    lines.push("host:    ok (ollama " + (ver.json.version || "?") + ")");
    const tags = await getJson("/api/tags", cfg.timeoutMs, cfg.baseUrl);
    const names = tags.ok ? (tags.json.models || []).map((m) => m.name) : [];
    lines.push("model:   " + (names.includes(model) ? "installed" : "MISSING — run: ollama pull " + model));
    if (!names.includes(model)) { console.error(lines.join("\n")); return 1; }
    const probe = await post("/v1/systemone", {
      model,
      state: "hello",
      questions: { is_greeting: { type: "noul", instructions: "Is this a greeting?", criteria: { true: "greeting", false: "not a greeting" } } },
    }, cfg.timeoutMs, cfg.baseUrl);
    if (!probe.ok) { console.error(lines.concat(["smoke:   FAILED " + probe.status + " " + probe.text.slice(0, 200)]).join("\n")); return 1; }
    const j = JSON.parse(probe.text);
    lines.push("smoke:   ok (is_greeting=" + j.answers.is_greeting.noul.toFixed(3) + ")");
    const prev = readLastEval();
    if (!prev) lines.push("eval:    never run — run: node nimble.mjs --eval");
    else if (prev.model !== model) lines.push("eval:    last run was " + prev.model + " (" + Math.round(prev.accuracy * 100) + "%) — stale for this model");
    else lines.push("eval:    " + prev.correct + "/" + prev.total + " (" + Math.round(prev.accuracy * 100) + "%) at " + prev.at);
    console.log(lines.join("\n"));
    return 0;
  }

  if (opts.flags.selftest) {
    const probe = await post("/v1/systemone", {
      model: opts.flags.model || cfg.model,
      state: "Hello there, how are you?",
      questions: {
        greeting: { type: "noul", instructions: "Does the text contain a greeting?", criteria: { true: "greeting", false: "no greeting" } },
        intent: { type: "choice", instructions: "What is the main intent?", criteria: { greet: "casual greeting", ask: "question", other: "other" } },
        politeness: { type: "score", instructions: "How polite is it?", criteria: ["rude", "neutral", "polite", "very polite"] },
      },
    }, cfg.timeoutMs, cfg.baseUrl);
    if (!probe.ok) die("selftest failed: " + probe.status + " " + probe.text, 1);
    const a = JSON.parse(probe.text).answers;
    const checks = [
      ["noul", typeof a.greeting.noul === "number" && a.greeting.noul > 0.5],
      ["choice", a.intent.choice === "greet"],
      ["score", typeof a.politeness.score === "number" && a.politeness.score >= 2],
    ];
    let bad = 0;
    for (const [n, ok] of checks) { if (!ok) bad++; console.log((ok ? "PASS " : "FAIL ") + n); }
    console.log(JSON.stringify(a));
    return bad ? 1 : 0;
  }

  let raw = opts.positional[0];
  if (raw === "-") raw = undefined;
  if (raw === undefined && !process.stdin.isTTY) {
    const chunks = [];
    for await (const c of process.stdin) chunks.push(c);
    raw = Buffer.concat(chunks).toString("utf8").trim();
  }
  if (!raw) die("no payload. Pass JSON as an argument or via stdin. See --help", 2);
  if (opts.flags["state-file"]) {
    if (!existsSync(opts.flags["state-file"])) die("state file not found: " + opts.flags["state-file"], 2);
    opts.flags.state = readFileSync(opts.flags["state-file"], "utf8");
  }

  const payload = buildPayload(raw, opts, cfg);
  if (opts.flags.dry) { console.log(JSON.stringify(payload, null, 2)); return 0; }

  const types = [...new Set(Object.values(payload.questions).map((q) => q.type))];
  const started = Date.now();
  const baseEntry = {
    ts: localIso(),
    agent,
    kind: "call",
    model: payload.model,
    types,
    qCount: Object.keys(payload.questions).length,
    stateChars: payload.state.length,
  };
  let res;
  try {
    res = await post("/v1/systemone", payload, cfg.timeoutMs, cfg.baseUrl);
  } catch (e) {
    logCall(cfg, { ...baseEntry, status: "error", durationMs: Date.now() - started, error: e.name === "AbortError" ? "timeout" : "unreachable" }, noLog);
    const hint = e.name === "AbortError"
      ? "timed out after " + cfg.timeoutMs + "ms (first load of a 9B model can take a while; raise timeoutMs in config.json)"
      : "cannot reach " + cfg.baseUrl + " — is ollama serve running? (" + e.message + ")";
    die(hint, 1);
  }
  const durationMs = Date.now() - started;
  if (opts.flags.debug) console.error("elapsed " + durationMs + "ms");
  if (!res.ok) {
    logCall(cfg, { ...baseEntry, status: "error", httpStatus: res.status, durationMs, error: res.text.slice(0, 200) }, noLog);
    die("HTTP " + res.status + ": " + res.text.slice(0, 500), 1);
  }
  let parsed;
  try { parsed = JSON.parse(res.text); } catch { die("non-JSON response: " + res.text.slice(0, 300), 1); }
  if (opts.flags.debug && parsed.usage) console.error("usage " + JSON.stringify(parsed.usage));
  logCall(cfg, {
    ...baseEntry,
    status: "ok",
    httpStatus: res.status,
    durationMs,
    inputTokens: parsed.usage ? parsed.usage.input_tokens : undefined,
  }, noLog);
  emit(parsed, opts);
  return 0;
}

try { process.exitCode = await main(); }
catch (e) { die("unexpected error: " + (e && e.stack ? e.stack : e), 1); }
