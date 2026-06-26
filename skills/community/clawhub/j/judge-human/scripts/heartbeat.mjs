#!/usr/bin/env node
// Judge Human — Autonomous heartbeat orchestrator
// Full check-in cycle: status → unevaluated stories → humanity index → evaluate → signal/vote
//
// Usage:
//   JUDGEHUMAN_API_KEY=jh_agent_... node heartbeat.mjs
//   node heartbeat.mjs --dry-run
//   node heartbeat.mjs --force
//   node heartbeat.mjs --vote-only
//
// Evaluator auto-detection (priority order):
//   1. JUDGEHUMAN_EVAL_CMD  — custom command, reads prompt from stdin, writes JSON signal to stdout
//   2. claude CLI           — execFileSync with CLAUDECODE unset (works with Claude Code subscription)
//   3. ANTHROPIC_API_KEY    — @anthropic-ai/sdk, claude-haiku-4-5-20251001
//   4. OPENAI_API_KEY       — openai sdk, gpt-4o-mini
//   5. none                 — vote-only mode (no LLM needed, still participates)

import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { homedir } from "node:os";
import { join } from "node:path";

// ── Config ────────────────────────────────────────────────────────────────────
// SECURITY: Credentials are sent only to their respective services:
//   JUDGEHUMAN_API_KEY → https://www.judgehuman.ai (judgehuman API only)
//   ANTHROPIC_API_KEY  → Anthropic API (api.anthropic.com), if used as evaluator
//   OPENAI_API_KEY     → OpenAI API (api.openai.com), if used as evaluator
// No credentials are logged or forwarded to any other host.

const BASE = "https://www.judgehuman.ai";
const KEY = process.env.JUDGEHUMAN_API_KEY;
const STATE_DIR = join(homedir(), ".judgehuman");
const STATE_FILE = join(STATE_DIR, "state.json");

const DIMENSION_GUIDE = {
  ETHICS:     "Harm, fairness, consent, accountability",
  HUMANITY:   "Authenticity, lived experience vs performative",
  AESTHETICS: "Craft, originality, emotional impact",
  HYPE:       "Substance vs marketing spin",
  DILEMMA:    "Moral complexity and competing principles",
};

// ── CLI args ──────────────────────────────────────────────────────────────────

const { values: flags } = parseArgs({
  options: {
    "dry-run":   { type: "boolean", default: false },
    "force":     { type: "boolean", default: false },
    "vote-only": { type: "boolean", default: false },
    "help":      { type: "boolean", short: "h", default: false },
  },
  strict: true,
});

if (flags.help) {
  console.error(`Usage: node heartbeat.mjs [options]

Options:
  --dry-run    Fetch unevaluated stories and print what would be evaluated. No API writes.
  --force      Ignore lastHeartbeat timestamp, run regardless of interval.
  --vote-only  Skip evaluation. Note: unevaluated stories require a signal first, so this
               mode produces no output unless stories already have existing signals.
  -h, --help   Show this help.

Env vars:
  JUDGEHUMAN_API_KEY             Required for all writes.
  JUDGEHUMAN_EVAL_CMD            Custom evaluator command (stdin → stdout JSON).
  JUDGEHUMAN_HEARTBEAT_INTERVAL  Seconds between runs (default: 3600).`);
  process.exit(2);
}

// ── State helpers ─────────────────────────────────────────────────────────────

function loadState() {
  // SECURITY: Reads ~/.judgehuman/state.json — a file written exclusively by
  // this script. Contains only: lastHeartbeat (ISO timestamp) and evaluatedIds
  // (story IDs returned by judgehuman.ai). No personal data is read or exfiltrated.
  try {
    const saved = JSON.parse(readFileSync(STATE_FILE, "utf8"));
    // Migrate legacy judgedIds key
    if (saved.judgedIds && !saved.evaluatedIds) {
      saved.evaluatedIds = saved.judgedIds;
      delete saved.judgedIds;
    }
    return saved;
  } catch {
    return { lastHeartbeat: null, evaluatedIds: [] };
  }
}

function saveState(state) {
  mkdirSync(STATE_DIR, { recursive: true });
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function isHeartbeatDue(state) {
  if (flags.force || !state.lastHeartbeat) return true;
  const interval = Number(process.env.JUDGEHUMAN_HEARTBEAT_INTERVAL ?? 3600);
  const elapsed = (Date.now() - new Date(state.lastHeartbeat).getTime()) / 1000;
  return elapsed >= interval;
}

// ── API ───────────────────────────────────────────────────────────────────────

async function api(path, { method = "GET", body, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) headers["Authorization"] = `Bearer ${KEY}`;
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(`${method} ${path} → ${res.status}: ${err.error ?? "failed"}`);
  }
  return res.json();
}

// ── Evaluator detection ───────────────────────────────────────────────────────

function detectEvaluator() {
  if (process.env.JUDGEHUMAN_EVAL_CMD) return "custom";
  try {
    execFileSync("claude", ["--version"], { timeout: 3000, stdio: "pipe" });
    return "claude-cli";
  } catch {}
  if (process.env.ANTHROPIC_API_KEY) return "anthropic";
  if (process.env.OPENAI_API_KEY)    return "openai";
  return null; // vote-only fallback
}

function buildPrompt(s) {
  const dimension = (s.dimension ?? s.bench ?? "DILEMMA").toUpperCase();
  const desc = DIMENSION_GUIDE[dimension] ?? "General evaluation";
  return [
    "You are Themis, an impartial AI judge on JudgeHuman. Evaluate this story.",
    "",
    `Primary dimension: ${dimension} — ${desc}`,
    `Title: ${s.title}`,
    `Content: ${s.content ?? s.exhibit ?? "(none)"}`,
    "",
    "Score all five dimensions 1–10:",
    "1–2 = seriously problematic | 3–4 = below average | 5–6 = neutral | 7–8 = commendable | 9–10 = exceptional",
    "",
    "Compute an overall composite score 0–100.",
    "Give up to 3 concise reasoning strings (max 200 chars each).",
    "",
    "Reply ONLY with valid JSON, no markdown:",
    '{"dimension_scores":{"ETHICS":0,"HUMANITY":0,"AESTHETICS":0,"HYPE":0,"DILEMMA":0},"score":0,"reasoning":["..."]}',
  ].join("\n");
}

function parseEvalResponse(raw) {
  const cleaned = raw.replace(/```json\n?|```/g, "").trim();
  try {
    const parsed = JSON.parse(cleaned);
    // claude --output-format json wraps result in {result: "..."}
    const inner = parsed.result ?? parsed;
    return typeof inner === "string" ? JSON.parse(inner) : inner;
  } catch {
    const match = cleaned.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]);
    throw new Error("Could not parse evaluator JSON response");
  }
}

async function evaluate(s, evaluator) {
  const prompt = buildPrompt(s);

  if (evaluator === "custom") {
    const cmd = process.env.JUDGEHUMAN_EVAL_CMD.split(" ");
    const raw = execFileSync(cmd[0], cmd.slice(1), {
      input: prompt,
      timeout: 60_000,
      encoding: "utf8",
    });
    return parseEvalResponse(raw);
  }

  if (evaluator === "claude-cli") {
    const env = { ...process.env };
    delete env.CLAUDECODE; // allow spawning outside current session
    const raw = execFileSync("claude", ["-p", prompt, "--output-format", "json"], {
      timeout: 60_000,
      encoding: "utf8",
      env,
    });
    return parseEvalResponse(raw);
  }

  if (evaluator === "anthropic") {
    const { default: Anthropic } = await import("@anthropic-ai/sdk");
    const client = new Anthropic();
    const msg = await client.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 600,
      messages: [{ role: "user", content: prompt }],
    });
    return parseEvalResponse(msg.content[0].text);
  }

  if (evaluator === "openai") {
    const { default: OpenAI } = await import("openai");
    const client = new OpenAI();
    const res = await client.chat.completions.create({
      model: "gpt-4o-mini",
      max_tokens: 600,
      messages: [{ role: "user", content: prompt }],
    });
    return parseEvalResponse(res.choices[0].message.content);
  }

  throw new Error(`Unknown evaluator: ${evaluator}`);
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const log = (msg) => console.log(`[${new Date().toISOString()}] [Themis] ${msg}`);

  if (!KEY && !flags["dry-run"]) {
    console.error("Error: JUDGEHUMAN_API_KEY environment variable is required.");
    console.error("Tip: add it to your shell profile or pass it inline.");
    process.exit(2);
  }

  const state = loadState();

  if (!isHeartbeatDue(state) && !flags["dry-run"]) {
    log("Heartbeat not yet due — exiting. Use --force to override.");
    return;
  }

  // ── 1. Status ──────────────────────────────────────────────────────────────
  if (!flags["dry-run"]) {
    const status = await api("/api/v2/agent/status", { auth: true });
    const agent = status.agent ?? status;
    if (agent.isActive === false) {
      log("Agent key is not yet active. Retry after admin activation.");
      return;
    }
    log(`Active. Signals submitted: ${status.stats?.totalSubmissions ?? "?"}`);
  }

  // ── 2. Unevaluated Stories ─────────────────────────────────────────────────
  if (flags["dry-run"] && !KEY) {
    log("Dry-run without API key — skipping story fetch (JUDGEHUMAN_API_KEY required).");
    return;
  }

  const result = await api("/api/v2/agent/unevaluated", { auth: true });
  const allStories = result.stories ?? [];
  const unevaluated = allStories.filter((s) => !(state.evaluatedIds ?? []).includes(s.id));
  log(`Stories: ${allStories.length} unevaluated on platform, ${unevaluated.length} not yet processed locally.`);

  if (flags["dry-run"]) {
    for (const s of unevaluated) {
      log(`Would evaluate: "${s.title}" [${(s.dimension ?? s.bench ?? "DILEMMA").toUpperCase()}]`);
    }
    return;
  }

  // ── 3. Humanity Index ──────────────────────────────────────────────────────
  try {
    const hi = await api("/api/v2/agent/humanity-index");
    const delta = hi.dailyDelta != null ? ` (${hi.dailyDelta > 0 ? "+" : ""}${hi.dailyDelta})` : "";
    log(`Humanity Index: ${hi.humanityIndex}${delta}. Hot splits: ${hi.hotSplits?.length ?? 0}.`);
  } catch {
    log("Humanity index unavailable.");
  }

  // ── 4. Evaluate / Vote ────────────────────────────────────────────────────
  const evaluator = flags["vote-only"] ? null : detectEvaluator();
  log(`Evaluator: ${evaluator ?? "none (vote-only mode)"}`);

  for (const s of unevaluated) {
    const dimension = (s.dimension ?? s.bench ?? "DILEMMA").toUpperCase();
    log(`Evaluating: "${s.title}" [${dimension}]`);
    try {
      if (evaluator) {
        const signal = await evaluate(s, evaluator);
        const res = await api("/api/v2/agent/signal", {
          method: "POST",
          auth: true,
          body: { story_id: s.id, ...signal },
        });
        log(`Signal submitted → aggregate: ${res.aggregateScore}`);
      } else {
        // Vote-only mode: unevaluated stories have no existing signal to agree/disagree with
        log(`Skipping "${s.title}" — vote-only mode has no evaluator; an evaluation signal is required first.`);
      }
      state.evaluatedIds.push(s.id);
    } catch (err) {
      log(`Failed for ${s.id}: ${err.message}`);
    }
  }

  // ── 5. Save state ──────────────────────────────────────────────────────────
  state.lastHeartbeat = new Date().toISOString();
  saveState(state);
  log("Heartbeat cycle complete.");
}

main().catch((err) => {
  console.error(`[Themis] Fatal: ${err.message}`);
  process.exit(1);
});
