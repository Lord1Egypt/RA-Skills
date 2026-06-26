import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  formatLocalTimestamp,
  nextOccurrenceForCalendar,
  occurrencesBetween,
  parseOnCalendarExpression
} from "./calendar.js";
import {
  buildReplyClassifierPrompt,
  classifyReplyIntent,
  parseSnoozeDuration
} from "./locale.js";
import { loadRuntime } from "./runtime/index.js";
import {
  detectSchedulerBackend,
  removeSchedulerWake,
  schedulerIsActive,
  upsertSchedulerWake
} from "./scheduler.js";
import {
  matchTone as vectorMatchTone,
  isAvailable as vectorTonesAvailable
} from "./vector-tones.js";

const ROOT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const PRESETS_DIR = path.join(ROOT_DIR, "presets");
const TONES_DIR = path.join(ROOT_DIR, "tones");
const RUNTIME_DIR = process.env.POKE_RUNTIME_DIR || path.join(ROOT_DIR, ".runtime");
const STATE_DIR = process.env.POKE_STATE_DIR || path.join(RUNTIME_DIR, "state");
const PATH_SETS_FILE = process.env.POKE_PATH_SETS_FILE || path.join(RUNTIME_DIR, "path-sets.json");
const DND_FILE = path.join(STATE_DIR, ".dnd.json");
const FLOOD_FILE = path.join(STATE_DIR, ".flood.json");
const VISIBILITY_FILE = path.join(STATE_DIR, ".visibility.json");
// Wall-clock helper. Returns the real time unless POKE_NOW_OVERRIDE is set to
// an ISO timestamp, in which case tests (or callers) can pin "now" to make
// time-of-day behavior (quiet hours, active hours, DND) deterministic.
function nowDate() {
  const override = process.env.POKE_NOW_OVERRIDE;
  if (override) {
    const parsed = new Date(override);
    if (!Number.isNaN(parsed.getTime())) return parsed;
  }
  return new Date();
}
const COMMITMENTS_FILE = path.join(STATE_DIR, "commitments.json");
const HISTORY_FILE = path.join(RUNTIME_DIR, "history.jsonl");
const ENTRY_SCRIPT = path.join(ROOT_DIR, "poke.js");
const DEFAULT_MAX_CATCHUP_RUNS = 10;

const L = {
  activeReminders: "=== Active Text Reminders ===",
  availableTones: "=== Available Tones ===",
  availablePresets: "=== Available Presets ===",
  savedPathSets: "=== Saved Path Sets ===",
  taskYes: "yes",
  taskNo: "no",
  noDescription: "no description",
  none: "(none)",
  unknown: "unknown",
  yes: "yes",
  no: "no",
  kindTask: "task",
  kindRemind: "reminder",
  task: "task",
  schedule: "schedule",
  pokes: "pokes",
  catchup: "catchup",
  timer: "timer",
  tone: "tone",
  onPong: "on-pong: command",
  preFire: "pre",
  postFire: "post",
  ifUnconfirmed: "if-unconfirmed: configured",
  preset: "preset",
  files: "files",
  updated: "updated",
  route: "route",
  state: "state",
  next: "next",
  created: "created",
  firstDelivered: "first_delivered",
  lastDelivered: "last_delivered",
  lastReply: "last_reply",
  backend: "backend",
  schemaVersion: "schema_version",
  pathSetSaved: (name, count) => `OK: Saved path set ${name} (${count} file${count === 1 ? "" : "s"})`,
  pathSetDeleted: (name) => `OK: Deleted path set ${name}`,
  confirmed: (id) => `OK: Confirmed ${id}`,
  cancelled: (id) => `OK: Cancelled ${id}`,
  cancelledAll: (count) => `OK: Cancelled ${count} reminder(s)`,
  reminderPrefix: (count, text) => (count > 1 ? `Reminder (#${count}): ${text}` : `Reminder: ${text}`),
  taskPrefix: (count) => count > 1 ? `Scheduled task (poke #${count}). Execute and deliver:` : "Scheduled task. Execute and deliver:",
  followupTaskPrefix: "Unconfirmed reminder follow-up. Execute and deliver:",
  helpText: `poke — text reminders via OS schedulers

Usage:
  poke --remind "text" --once 30m --channel CH --target TGT

Content (pick one):
  --remind "text"            Canonical reminder intent, phrased freshly on delivery
  --task "prompt"            Agent task prompt
  --reply "user message"     Process an inbound reply against scoped reminders

Scheduling:
  --once <duration>          One-shot after delay (30s, 30m, 2h, 1d)
  --at "HH:MM"               One-shot today/tomorrow at local time
  --at "YYYY-MM-DD HH:MM"    One-shot at exact local date/time
  --on-calendar "EXPR"       Recurrent calendar expression

Options:
  --max-pokes N
  --agent ID
  --channel CH               Comma-separated for multi-channel delivery
  --target TGT               Comma-separated for multi-target delivery
  --tone "name" | --tone "a,b,c"
  --escalation-intervals "10,5,3"
  --quiet-hours "22:00-08:00" Per-reminder: suppress delivery during this window
  --active-hours "08:00-22:00" Only deliver DURING these hours (inverse of quiet-hours)
  --urgent                   Bypass quiet hours, active hours, and DND
  --dnd                      Show current DND status
  --dnd-until "30m" | "14:00" Enable DND globally for duration/time
  --dnd-off                  Disable DND
  --task-interval "30m"      Minimum interval between task executions
  --visibility-set CH MODE   Set channel visibility (all/alerts/urgent)
  --visibility               Show visibility settings
  --commit "reason"           Create a follow-up commitment
  --due "30m"                 Commitment due duration (default: 1d)
  --kind TYPE                 Commitment kind (event_check_in/deadline_check/care_check_in/open_loop)
  --sensitivity LVL           Commitment sensitivity (routine/personal/care)
  --commitments               List pending commitments
  --commit-done ID            Mark commitment completed
  --commit-cancel ID          Cancel commitment
  --depends-on ID            Don't fire until dependency is confirmed
  --vector-tones             Match tone by embedding similarity (needs ollama)
  --pre-cmd CMD             Argv command before delivery (no shell; whitespace
                            tokenizer with '/" quotes, or pass JSON array)
  --post-cmd CMD            Argv command after delivery (same parsing as --pre-cmd)
  --pre-task PROMPT         Agent-prompt before delivery, delivered to the
                            origin channel/target (e.g. "Warm up the cache")
  --post-task PROMPT        Agent-prompt after delivery
  --on-pong-command CMD     Argv command when the user replies (same parsing)
  --if-unconfirmed-remind TXT
  --if-unconfirmed-task TXT
  --if-unconfirmed-command CMD
  --if-unconfirmed-after DUR   (works with --once and --on-calendar)
  --if-unconfirmed-after-pokes N
  --preset NAME
  --persistent               Alias for catchup=coalesce
  --flippant                 Alias for catchup=none

Replies:
  "done" / "finished"        Confirms and closes the reminder
  "cancel" / "stop"          Cancels the reminder
  "snooze" / "snooze 30m"    Delays the reminder (default 15m)
  "later" / "on it"          Acknowledges, suppresses follow-up

Path sets:
  --paths-save NAME --file PATH [--file PATH ...]
  --paths-show NAME
  --paths-delete NAME
  --paths-list

Management:
  --list
  --latest
  --show ID
  --confirm ID
  --cancel ID
  --cancel-all
  --history [N]              Tail the last N lifecycle events (default 50)
  --stats                    Active-reminder + history-based aggregate counts
  --dry-run                  Validate + show what would be scheduled; no write
`,
};
function ensureDirectory(directory) {
  fs.mkdirSync(directory, { recursive: true });
}

function readJson(filePath, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

function writeJson(filePath, data) {
  ensureDirectory(path.dirname(filePath));
  // Atomic write: tempfile + rename. Survives crashes and concurrent fires
  // mid-write (S2.7/S2.8 risk class). Same-directory rename is atomic on
  // POSIX and on NTFS via ReplaceFile.
  const tempPath = `${filePath}.tmp-${process.pid}-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
  fs.writeFileSync(tempPath, JSON.stringify(data, null, 2));
  fs.renameSync(tempPath, filePath);
}

function reminderFile(id) {
  return path.join(STATE_DIR, `${id}.json`);
}

// ── Do Not Disturb (DND) ──────────────────────────────────────────────
// Global, dynamic suppression — unlike quiet_hours which is per-reminder
// and static. DND applies to ALL non-urgent reminders until it expires.

function loadDnd() {
  const data = readJson(DND_FILE, null);
  if (!data || typeof data !== "object") return null;
  if (data.until && new Date(data.until).getTime() <= Date.now()) return null;
  return data;
}

function saveDnd(data) {
  ensureDirectory(STATE_DIR);
  if (!data) {
    try { fs.unlinkSync(DND_FILE); } catch {}
    return;
  }
  writeJson(DND_FILE, data);
}

// Resolve the effective quiet-hours window for a given reminder at fire time.
// Quiet hours are per-reminder only — there is no global default. The "none"
// sentinel is kept for backward compat with state files written by older
// builds (when --no-quiet-hours opted out of a global default).
//   state.quiet_hours === "none"         → no window
//   state.quiet_hours is a "HH:MM-HH:MM" → that window
//   state.quiet_hours is null/empty      → no window
function effectiveQuietHours(state) {
  if (!state.quiet_hours || state.quiet_hours === "none") return null;
  return state.quiet_hours;
}

function isDndActive(now = new Date()) {
  const dnd = loadDnd();
  if (!dnd) return false;
  if (dnd.until && new Date(dnd.until).getTime() <= now.getTime()) return false;
  return true;
}

function dndStatusText() {
  const dnd = loadDnd();
  if (!dnd) return "DND is off.";
  const until = dnd.until ? new Date(dnd.until) : null;
  if (until) {
    const remaining = until.getTime() - Date.now();
    if (remaining <= 0) return "DND is off.";
    const mins = Math.ceil(remaining / 60000);
    const hours = Math.floor(mins / 60);
    const remMins = mins % 60;
    const timeStr = hours > 0 ? `${hours}h${remMins > 0 ? ` ${remMins}m` : ""}` : `${mins}m`;
    return `DND is ON until ${until.toLocaleTimeString()} (${timeStr} remaining).`;
  }
  return "DND is ON (no expiry set).";
}

function parseDndDuration(raw) {
  const trimmed = String(raw || "").trim();
  if (!trimmed) return new Date(Date.now() + 3600_000).toISOString();
  const durationMatch = trimmed.match(/^(\d+)([smhd])$/i);
  if (durationMatch) {
    const count = Number.parseInt(durationMatch[1], 10);
    const unit = durationMatch[2].toLowerCase();
    const multipliers = { s: 1000, m: 60_000, h: 3_600_000, d: 86_400_000 };
    return new Date(Date.now() + count * multipliers[unit]).toISOString();
  }
  return parseAtInput(trimmed).toISOString();
}

function sanitizeId(id) {
  return String(id).replace(/[^A-Za-z0-9_.-]/g, "-");
}

function generateId() {
  const now = new Date();
  const timestamp = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, "0"),
    String(now.getDate()).padStart(2, "0")
  ].join("");
  const clock = [String(now.getHours()).padStart(2, "0"), String(now.getMinutes()).padStart(2, "0"), String(now.getSeconds()).padStart(2, "0")].join("");
  const random = Math.random().toString(16).slice(2, 10);
  return `tr-${timestamp}-${clock}-${random}`;
}

function parseDuration(duration) {
  const match = String(duration || "").trim().match(/^(\d+)([smhd])$/i);
  if (!match) {
    throw new Error(`Invalid duration '${duration}' — use 30m, 2h, 1d, or 30s`);
  }
  const count = Number.parseInt(match[1], 10);
  const unit = match[2].toLowerCase();
  switch (unit) {
    case "s":
      return count;
    case "m":
      return count * 60;
    case "h":
      return count * 3600;
    case "d":
      return count * 86400;
    default:
      throw new Error(`Invalid duration '${duration}'`);
  }
}

function parseAtInput(input) {
  const trimmed = String(input || "").trim();
  if (/^\d{2}:\d{2}$/.test(trimmed)) {
    const now = new Date();
    const [hour, minute] = trimmed.split(":").map((value) => Number.parseInt(value, 10));
    let candidate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour, minute, 0, 0);
    if (candidate.getTime() <= now.getTime()) {
      candidate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, hour, minute, 0, 0);
    }
    return candidate;
  }
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(trimmed)) {
    const [datePart, timePart] = trimmed.split(" ");
    const [year, month, day] = datePart.split("-").map((value) => Number.parseInt(value, 10));
    const [hour, minute] = timePart.split(":").map((value) => Number.parseInt(value, 10));
    return new Date(year, month - 1, day, hour, minute, 0, 0);
  }
  throw new Error(`Invalid time format '${input}'`);
}

// Tokenize a shell-like string into argv. Honors single/double quotes and
// backslash escapes. NO shell metachar expansion — no $VAR, pipes, redirects,
// or subshells. If you need any of those, wrap the command in a script and
// invoke that script's path instead.
function tokenizeShellLike(input) {
  const s = String(input || "");
  const out = [];
  let cur = "";
  let curStarted = false;
  let quote = null;
  for (let i = 0; i < s.length; i += 1) {
    const c = s[i];
    if (quote) {
      if (c === quote) { quote = null; continue; }
      if (c === "\\" && quote === "\"" && i + 1 < s.length) {
        cur += s[i + 1];
        i += 1;
        continue;
      }
      cur += c;
      continue;
    }
    if (c === "\"" || c === "'") {
      quote = c;
      curStarted = true;
      continue;
    }
    if (c === "\\" && i + 1 < s.length) {
      cur += s[i + 1];
      curStarted = true;
      i += 1;
      continue;
    }
    if (/\s/.test(c)) {
      if (curStarted) { out.push(cur); cur = ""; curStarted = false; }
      continue;
    }
    cur += c;
    curStarted = true;
  }
  if (quote) throw new Error(`Unclosed ${quote === "'" ? "single" : "double"} quote in command`);
  if (curStarted) out.push(cur);
  return out;
}

// Parse a --pre-cmd/--post-cmd value: a JSON array of strings (explicit) or a
// shell-like whitespace-tokenized string (friendly).
function parseArgvFlagValue(raw, flagName) {
  const s = String(raw || "").trim();
  if (!s) throw new Error(`${flagName} requires a non-empty value`);
  if (s.startsWith("[")) {
    let parsed;
    try { parsed = JSON.parse(s); }
    catch (err) { throw new Error(`${flagName} JSON parse failed: ${err.message}`); }
    if (!Array.isArray(parsed) || !parsed.length || !parsed.every((x) => typeof x === "string")) {
      throw new Error(`${flagName} JSON must be a non-empty array of strings`);
    }
    return parsed;
  }
  const argv = tokenizeShellLike(s);
  if (!argv.length) throw new Error(`${flagName} value tokenized to nothing`);
  return argv;
}

// Hooks run with a deliberately minimal environment — NOT the full parent
// process.env. A reminder side-effect script has no need for ambient secrets
// or tokens that happen to be in poke's environment. HOOK_ENV_BASE keeps the
// subprocess functional (path resolution, locale, timezone); anything beyond
// that is opt-in per reminder via --hook-env VAR.
const HOOK_ENV_BASE = ["PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "TZ"];

function buildStageEnv(state, hookName, replyAction) {
  const allow = new Set([...HOOK_ENV_BASE, ...(Array.isArray(state.hook_env) ? state.hook_env : [])]);
  const env = {};
  for (const key of allow) {
    if (process.env[key] !== undefined) env[key] = process.env[key];
  }
  return {
    ...env,
    POKE_HOOK: hookName,
    POKE_ID: state.id,
    POKE_TEXT: state.task || state.remind || "",
    POKE_AGENT: state.agent || "",
    POKE_CHANNEL: state.channel || "",
    POKE_TARGET: state.target || "",
    POKE_ORIGIN_CHANNEL: state.origin_channel || state.channel || "",
    POKE_ORIGIN_TARGET: state.origin_target || state.target || "",
    POKE_COUNT: String(state.cycle_poke_count || state.poke_count || 0),
    POKE_REPLY_ACTION: replyAction || "",
    POKE_STATE_FILE: reminderFile(state.id)
  };
}

function logHookOutcome(state, hookName, outcome) {
  try {
    const logPath = path.join(RUNTIME_DIR, "hook-log.jsonl");
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    const entry = {
      ts: new Date().toISOString(),
      reminder_id: state.id,
      hook: hookName,
      ...outcome
    };
    fs.appendFileSync(logPath, JSON.stringify(entry) + "\n");
  } catch {
    // Logging is best-effort; never block a hook on its own log write.
  }
}

// Run one hook stage. A stage is either:
//   { type: "cmd", argv: ["program", "arg", ...] }     — argv exec, no shell
//   { type: "task", prompt: "..." }                    — agent-prompt
// Failures are logged and swallowed — a broken hook must not derail the
// delivery loop.
function runHookStage(state, hookName, stage, runtime = null, replyAction = "") {
  if (!stage) return;
  const env = buildStageEnv(state, hookName, replyAction);

  if (stage.type === "cmd") {
    const argv = Array.isArray(stage.argv) ? stage.argv : [];
    if (!argv.length) {
      logHookOutcome(state, hookName, { type: "cmd", ok: false, message: "empty argv" });
      return;
    }
    const [program, ...args] = argv;
    try {
      const stdout = execFileSync(program, args, { env, timeout: 120_000, encoding: "utf8" });
      logHookOutcome(state, hookName, { type: "cmd", ok: true, exit_code: 0, stdout });
    } catch (err) {
      logHookOutcome(state, hookName, {
        type: "cmd",
        ok: false,
        exit_code: typeof err.status === "number" ? err.status : -1,
        stdout: err.stdout ? err.stdout.toString() : "",
        stderr: err.stderr ? err.stderr.toString() : "",
        message: err.message
      });
    }
    return;
  }

  if (stage.type === "task") {
    if (!runtime) {
      logHookOutcome(state, hookName, { type: "task", ok: false, message: "no runtime available for agent stage" });
      return;
    }
    try {
      const agent = state.agent || runtime.defaultAgentId();
      const channel = state.origin_channel || state.channel;
      const target = state.origin_target || state.target;
      runtime.deliver({
        agent,
        channel,
        target,
        prompt: stage.prompt,
        sessionHint: target || channel
      });
      logHookOutcome(state, hookName, { type: "task", ok: true });
    } catch (err) {
      logHookOutcome(state, hookName, { type: "task", ok: false, message: err.message });
    }
    return;
  }

  logHookOutcome(state, hookName, { ok: false, message: `unknown stage type: ${stage.type}` });
}

// History — append-only JSONL of lifecycle events. Survives confirm/cancel
// (the reminder file gets deleted on terminal states; the history line stays).
function appendHistory(entry) {
  try {
    ensureDirectory(path.dirname(HISTORY_FILE));
    const line = JSON.stringify({ ts: new Date().toISOString(), ...entry });
    fs.appendFileSync(HISTORY_FILE, `${line}\n`);
  } catch {
    // History is best-effort; never block primary flow on its log write.
  }
}

function tailHistory(limit) {
  if (!fs.existsSync(HISTORY_FILE)) return [];
  const lines = fs.readFileSync(HISTORY_FILE, "utf8").split("\n").filter(Boolean);
  return lines.slice(-Math.max(1, limit));
}

// --stats — quick aggregate over the active reminders + recent history.
function formatStats(activeReminders) {
  const history = fs.existsSync(HISTORY_FILE)
    ? fs.readFileSync(HISTORY_FILE, "utf8").split("\n").filter(Boolean).map((l) => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean)
    : [];
  const counts = {};
  for (const h of history) counts[h.event] = (counts[h.event] || 0) + 1;

  // Confirm latency: time between last delivery and confirm, per id.
  const lastDelivered = new Map();
  const latencies = [];
  for (const h of history) {
    if (h.event === "delivered" && h.id) lastDelivered.set(h.id, new Date(h.ts).getTime());
    else if (h.event === "confirm" && h.id && lastDelivered.has(h.id)) {
      latencies.push(new Date(h.ts).getTime() - lastDelivered.get(h.id));
    }
  }
  const meanLatencyMs = latencies.length
    ? Math.round(latencies.reduce((a, b) => a + b, 0) / latencies.length)
    : null;

  const lines = ["=== Poke Stats ===", `active: ${activeReminders.length}`];
  for (const k of ["created", "delivered", "confirm", "cancel", "snooze", "followup", "suppressed"]) {
    lines.push(`${k}: ${counts[k] || 0}`);
  }
  lines.push(`mean confirm latency: ${meanLatencyMs == null ? "(no data)" : `${Math.round(meanLatencyMs / 1000)}s`}`);
  return lines.join("\n");
}

function stageSummary(stage) {
  if (!stage) return "-";
  if (stage.type === "cmd") return `cmd: ${(stage.argv || []).join(" ")}`;
  if (stage.type === "task") return `task: ${String(stage.prompt || "").slice(0, 80)}`;
  return JSON.stringify(stage);
}

// Migrate legacy state-file fields onto the new stage shape. Safe to call on
// already-migrated states (no-op).
function migrateLegacyStages(state) {
  if (!state) return state;
  if (!state.pre_stage && state.pre_fire_command) {
    try { state.pre_stage = { type: "cmd", argv: tokenizeShellLike(state.pre_fire_command) }; }
    catch { /* leave legacy field as-is on parse error */ }
  }
  if (!state.post_stage && state.post_fire_command) {
    try { state.post_stage = { type: "cmd", argv: tokenizeShellLike(state.post_fire_command) }; }
    catch { /* leave legacy field as-is on parse error */ }
  }
  if (!state.pong_stage && state.pong_command) {
    try { state.pong_stage = { type: "cmd", argv: tokenizeShellLike(state.pong_command) }; }
    catch { /* leave legacy field as-is on parse error */ }
  }
  return state;
}

function pathSetStore() {
  const data = readJson(PATH_SETS_FILE, { version: 1, sets: {} });
  if (!data.sets || typeof data.sets !== "object") data.sets = {};
  return data;
}

function validatePathSetName(name) {
  if (!/^[A-Za-z0-9_.-]+$/.test(name)) {
    throw new Error(`Invalid path set name '${name}' — use letters, numbers, ., _, -`);
  }
}

function normalizeSavedPath(filePath) {
  if (String(filePath).startsWith("~/")) {
    return path.join(os.homedir(), String(filePath).slice(2));
  }
  return path.resolve(String(filePath));
}

function savePathSet(name, files) {
  validatePathSetName(name);
  if (!files.length) {
    throw new Error("--paths-save requires at least one --file");
  }
  const store = pathSetStore();
  store.sets[name] = {
    files: [...new Set(files.map(normalizeSavedPath))],
    updated_at: new Date().toISOString()
  };
  writeJson(PATH_SETS_FILE, store);
}

function showPathSet(name) {
  validatePathSetName(name);
  const store = pathSetStore();
  return store.sets[name] || null;
}

function listPathSets() {
  const store = pathSetStore();
  return Object.entries(store.sets).sort((left, right) => left[0].localeCompare(right[0]));
}

function deletePathSet(name) {
  validatePathSetName(name);
  const store = pathSetStore();
  if (!store.sets[name]) {
    throw new Error(`No saved path set: ${name}`);
  }
  delete store.sets[name];
  writeJson(PATH_SETS_FILE, store);
}

function expandPathPlaceholders(text) {
  const value = String(text || "");
  const regex = /\{\{\s*paths:([A-Za-z0-9_.-]+)\s*\}\}/g;
  if (!regex.test(value)) return value;
  regex.lastIndex = 0;
  const store = pathSetStore();
  return value.replace(regex, (_, name) => {
    const entry = store.sets[name];
    if (!entry || !Array.isArray(entry.files) || entry.files.length === 0) {
      throw new Error(
        `Missing saved path set '${name}'. Register it with --paths-save ${name} --file <path> [...].`
      );
    }
    return entry.files.map((filePath) => `- ${filePath}`).join("\n");
  });
}

function loadToneFiles() {
  const results = [];
  if (fs.existsSync(TONES_DIR)) {
    for (const entry of fs.readdirSync(TONES_DIR).sort()) {
      if (!entry.endsWith(".json")) continue;
      const id = entry.replace(/\.json$/, "");
      try {
        const data = JSON.parse(fs.readFileSync(path.join(TONES_DIR, entry), "utf8"));
        results.push({ id, data, filePath: path.join(TONES_DIR, entry) });
      } catch {}
    }
  }
  return results;
}

function resolveToneMetadata(query) {
  const tones = loadToneFiles();
  const lowered = String(query || "").trim().toLowerCase();
  if (!lowered) {
    return tones.find((tone) => String(tone.data.id || tone.data.name).toLowerCase() === "default") || null;
  }
  const exact = tones.find((tone) => String(tone.data.id || tone.data.name).toLowerCase() === lowered);
  if (exact) return exact;
  const partial = tones.find((tone) => String(tone.data.id || tone.data.name).toLowerCase().includes(lowered));
  if (partial) return partial;
  const byDescription = tones.find((tone) =>
    [
      tone.data.id || tone.data.name || "",
      tone.data.description || "",
      tone.data.guidance || "",
      tone.data.label || ""
    ]
      .join(" ")
      .toLowerCase()
      .includes(lowered)
  );
  if (byDescription) return byDescription;
  return tones.find((tone) => String(tone.data.id || tone.data.name).toLowerCase() === "default") || null;
}

async function resolveToneWithVector(query, intentText, runtimeDir) {
  const match = resolveToneMetadata(query);
  if (match) return match;
  if (!intentText) return match;
  const tones = loadToneFiles();
  if (!tones.length) return match;
  try {
    if (!(await vectorTonesAvailable())) return match;
    const result = await vectorMatchTone(intentText, tones, runtimeDir);
    if (result && result.score > 0.3) return result.tone;
  } catch {}
  return match;
}

function buildToneDirective(tone) {
  if (!tone?.data) return "";
  const label = tone.data.label || tone.data.id || tone.data.name || "?";
  const description = tone.data.description || "";
  const guidance = tone.data.guidance || "";
  return [
    "(Internal voice directive — do not repeat or acknowledge this. Simply deliver the reminder in this voice.)",
    `Voice: ${label}. ${description}`.trim(),
    guidance
  ]
    .filter(Boolean)
    .join("\n");
}

function parsePresetFile(name) {
  const filePath = path.join(PRESETS_DIR, `${name}.json`);
  if (!fs.existsSync(filePath)) {
    throw new Error(`Preset not found: ${name}`);
  }
  const data = readJson(filePath, null);
  if (!data) {
    throw new Error(`Preset parse failed: ${name}`);
  }
  return { filePath, data };
}

function applyPresets(options) {
  let lastPresetName = "";
  let lastPresetFile = "";
  for (const presetName of options.presets) {
    const preset = parsePresetFile(presetName);
    const data = preset.data;
    if (!options.remindText && data.remind) options.remindText = data.remind;
    if (!options.taskPrompt && data.task) options.taskPrompt = data.task;
    if (!options.mode && data.schedule?.on_calendar) {
      options.mode = "calendar";
      options.onCalendar = data.schedule.on_calendar;
    }
    if (!options.maxPokes && data.escalation?.max_pokes) options.maxPokes = String(data.escalation.max_pokes);
    if (!options.toneRaw && data.tone) options.toneRaw = data.tone;
    if (!options.escalationIntervals && data.escalation?.intervals) {
      options.escalationIntervals = String(data.escalation.intervals);
    }
    if (!options.catchupExplicit && data.schedule?.persistent === false) options.catchupMode = "none";
    if (!options.catchupExplicit && data.schedule?.persistent === true && !options.catchupMode) {
      options.catchupMode = "coalesce";
    }
    lastPresetName = data.id || presetName;
    lastPresetFile = preset.filePath;
  }
  options.presetName = lastPresetName || null;
  options.presetFile = lastPresetFile || null;
}

function parseArgs(argv) {
  const options = {
    remindText: "",
    taskPrompt: "",
    onceDelay: "",
    atTime: "",
    onCalendar: "",
    replyText: "",
    followupRemind: "",
    followupTask: "",
    followupCommand: "",
    followupAfter: "",
    followupAfterPokes: "",
    preStage: null,
    postStage: null,
    pongStage: null,
    activeHours: "",
    taskInterval: "",
    commitReason: "",
    commitDue: "",
    commitSensitivity: "",
    commitKind: "",
    commitId: "",
    maxPokes: "",
    agent: "",
    channel: "",
    target: "",
    from: "",
    presets: [],
    mode: "",
    id: "",
    toneRaw: "",
    escalationIntervals: "",
    pathSetName: "",
    pathFiles: [],
    hookEnv: [],
    catchupMode: "",
    catchupExplicit: false,
    maxCatchupRuns: DEFAULT_MAX_CATCHUP_RUNS,
    dndUntil: "",
    dryRun: false,
    historyLimit: 0
  };

  const nextValue = (index, label) => {
    if (index + 1 >= argv.length) throw new Error(`Missing value for ${label}`);
    return argv[index + 1];
  };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    switch (current) {
      case "--remind":
        options.remindText = nextValue(index, current);
        index += 1;
        break;
      case "--task":
        options.taskPrompt = nextValue(index, current);
        index += 1;
        break;
      case "--once":
        options.mode = "once";
        options.onceDelay = nextValue(index, current);
        index += 1;
        break;
      case "--at":
        options.mode = "at";
        options.atTime = nextValue(index, current);
        index += 1;
        break;
      case "--on-calendar":
        options.mode = "calendar";
        options.onCalendar = nextValue(index, current);
        index += 1;
        break;
      case "--reply":
        options.mode = "reply";
        options.replyText = nextValue(index, current);
        index += 1;
        break;
      case "--reply-stdin":
        options.mode = "reply";
        options.replyText = "@stdin";
        break;
      case "--from":
        options.from = nextValue(index, current);
        index += 1;
        break;
      case "--persistent":
        if (!options.catchupExplicit) options.catchupMode = "coalesce";
        break;
      case "--flippant":
        options.catchupMode = "none";
        options.catchupExplicit = true;
        break;
      case "--catchup":
        options.catchupMode = nextValue(index, current);
        options.catchupExplicit = true;
        index += 1;
        break;
      case "--max-catchup-runs":
        options.maxCatchupRuns = Number.parseInt(nextValue(index, current), 10);
        index += 1;
        break;
      case "--max-pokes":
        options.maxPokes = nextValue(index, current);
        index += 1;
        break;
      case "--agent":
        options.agent = nextValue(index, current);
        index += 1;
        break;
      case "--channel":
        options.channel = nextValue(index, current);
        index += 1;
        break;
      case "--target":
        options.target = nextValue(index, current);
        index += 1;
        break;
      case "--pre-cmd":
        options.preStage = { type: "cmd", argv: parseArgvFlagValue(nextValue(index, current), "--pre-cmd") };
        index += 1;
        break;
      case "--post-cmd":
        options.postStage = { type: "cmd", argv: parseArgvFlagValue(nextValue(index, current), "--post-cmd") };
        index += 1;
        break;
      case "--pre-task":
        options.preStage = { type: "task", prompt: nextValue(index, current) };
        index += 1;
        break;
      case "--post-task":
        options.postStage = { type: "task", prompt: nextValue(index, current) };
        index += 1;
        break;
      case "--on-pong-command":
        options.pongStage = { type: "cmd", argv: parseArgvFlagValue(nextValue(index, current), "--on-pong-command") };
        index += 1;
        break;
      case "--if-unconfirmed-remind":
        options.followupRemind = nextValue(index, current);
        index += 1;
        break;
      case "--if-unconfirmed-task":
        options.followupTask = nextValue(index, current);
        index += 1;
        break;
      case "--if-unconfirmed-command":
      case "--on-no-pong-command":
        options.followupCommand = nextValue(index, current);
        index += 1;
        break;
      case "--if-unconfirmed-after":
        options.followupAfter = nextValue(index, current);
        index += 1;
        break;
      case "--if-unconfirmed-after-pokes":
        options.followupAfterPokes = nextValue(index, current);
        index += 1;
        break;
      case "--preset":
        options.presets.push(nextValue(index, current));
        index += 1;
        break;
      case "--file":
        options.pathFiles.push(nextValue(index, current));
        index += 1;
        break;
      case "--hook-env":
        options.hookEnv.push(nextValue(index, current));
        index += 1;
        break;
      case "--tone":
        options.toneRaw = nextValue(index, current);
        index += 1;
        break;
      case "--vector-tones":
        options.vectorTones = true;
        break;
      case "--escalation-intervals":
        options.escalationIntervals = nextValue(index, current);
        index += 1;
        break;
      case "--quiet-hours":
        options.quietHours = nextValue(index, current);
        index += 1;
        break;
      case "--no-quiet-hours":
        // Explicit opt-out from the global default for THIS reminder only.
        // Stored as the sentinel "none" so effectiveQuietHours can tell it
        // apart from "not set / inherit default".
        options.quietHours = "none";
        break;
      case "--active-hours":
        options.activeHours = nextValue(index, current);
        index += 1;
        break;
      case "--task-interval":
        options.taskInterval = nextValue(index, current);
        index += 1;
        break;
      case "--visibility":
        options.mode = "visibility";
        break;
      case "--visibility-set":
        options.mode = "visibility-set";
        options.visibilityChannel = nextValue(index, current);
        index += 1;
        options.visibilityMode = nextValue(index, current);
        index += 1;
        break;
      case "--commit":
        options.mode = "commit";
        options.commitReason = nextValue(index, current);
        index += 1;
        break;
      case "--commitments":
        options.mode = "commitments";
        break;
      case "--commit-done":
        options.mode = "commit-done";
        options.commitId = nextValue(index, current);
        index += 1;
        break;
      case "--commit-cancel":
        options.mode = "commit-cancel";
        options.commitId = nextValue(index, current);
        index += 1;
        break;
      case "--due":
        options.commitDue = nextValue(index, current);
        index += 1;
        break;
      case "--sensitivity":
        options.commitSensitivity = nextValue(index, current);
        index += 1;
        break;
      case "--kind":
        options.commitKind = nextValue(index, current);
        index += 1;
        break;
      case "--depends-on":
        options.dependsOn = nextValue(index, current);
        index += 1;
        break;
      case "--urgent":
        options.urgent = true;
        break;
      case "--paths-save":
        options.mode = "paths-save";
        options.pathSetName = nextValue(index, current);
        index += 1;
        break;
      case "--paths-show":
        options.mode = "paths-show";
        options.pathSetName = nextValue(index, current);
        index += 1;
        break;
      case "--paths-delete":
      case "--paths-remove":
        options.mode = "paths-delete";
        options.pathSetName = nextValue(index, current);
        index += 1;
        break;
      case "--paths-list":
        options.mode = "paths-list";
        break;
      case "--list":
        options.mode = "list";
        break;
      case "--latest":
        options.mode = "latest";
        break;
      case "--show":
        options.mode = "show";
        options.id = nextValue(index, current);
        index += 1;
        break;
      case "--tones":
        options.mode = "tones";
        break;
      case "--presets":
        options.mode = "presets";
        break;
      case "--dry-run":
        options.dryRun = true;
        break;
      case "--history":
        options.mode = "history";
        if (index + 1 < argv.length && /^\d+$/.test(argv[index + 1])) {
          options.historyLimit = Number.parseInt(argv[index + 1], 10);
          index += 1;
        }
        break;
      case "--stats":
        options.mode = "stats";
        break;
      case "--confirm":
        options.mode = "confirm";
        options.id = nextValue(index, current);
        index += 1;
        break;
      case "--cancel":
        options.mode = "cancel";
        options.id = nextValue(index, current);
        index += 1;
        break;
      case "--cancel-all":
        options.mode = "cancel-all";
        break;
      case "--dnd":
        options.mode = "dnd";
        break;
      case "--dnd-until":
        options.mode = "dnd-on";
        options.dndUntil = nextValue(index, current);
        index += 1;
        break;
      case "--dnd-off":
        options.mode = "dnd-off";
        break;
      case "--deliver":
        options.mode = "deliver";
        options.id = nextValue(index, current);
        index += 1;
        break;
      case "--help":
      case "-h":
        options.mode = "help";
        break;
      default:
        throw new Error(`Unknown argument: ${current}`);
    }
  }

  if (!options.catchupMode) options.catchupMode = "coalesce";
  return options;
}

function ensureStateDir() {
  ensureDirectory(STATE_DIR);
}

function stateFiles() {
  ensureStateDir();
  return fs
    .readdirSync(STATE_DIR)
    .filter((entry) => /^tr-[A-Za-z0-9_.-]+\.json$/.test(entry))
    .map((entry) => path.join(STATE_DIR, entry))
    .sort();
}

function loadReminder(id) {
  return migrateLegacyStages(readJson(reminderFile(id), null));
}

function saveReminder(state) {
  writeJson(reminderFile(state.id), state);
}

function deleteReminder(state) {
  try {
    fs.unlinkSync(reminderFile(state.id));
  } catch {}
}

function queryReminders({ channel = "", target = "", agent = "" } = {}) {
  return stateFiles()
    .map((filePath) => migrateLegacyStages(readJson(filePath, null)))
    .filter(Boolean)
    .filter((state) => !state.confirmed && !state.cancelled)
    .filter((state) => !channel || state.channel === channel)
    .filter((state) => !target || state.target === target)
    .filter((state) => !agent || !state.agent || state.agent === agent)
    .sort((left, right) => {
      const leftKey = left.last_delivered || left.created_at || "";
      const rightKey = right.last_delivered || right.created_at || "";
      return rightKey.localeCompare(leftKey) || right.id.localeCompare(left.id);
    });
}

function summaryLine(state) {
  const pack = L;
  const kind = state.kind === "task" ? pack.kindTask : pack.kindRemind;
  const text = state.task || state.remind || "";
  const schedule =
    state.schedule_type === "calendar" ? state.on_calendar : state.schedule_input || state.schedule_type || "once";
  const timerActive = state.scheduler_handle
    ? schedulerIsActive({
        backend: state.scheduler_backend,
        stateDir: STATE_DIR,
        reminderId: state.id,
        schedulerHandle: state.scheduler_handle
      })
    : false;
  const tone = state.current_tone || state.tone || "";
  const lines = [
    `  ${state.id} (${kind})`,
    `    ${text}`,
    `    ${pack.schedule}: ${schedule} | ${pack.pokes}: ${state.cycle_poke_count || 0}/${state.max_pokes === -1 ? "inf" : state.max_pokes} | ${pack.catchup}: ${state.catchup} | ${pack.timer}: ${timerActive ? pack.yes : pack.no}`
  ];
  if (tone) lines.push(`    ${pack.tone}: ${tone}`);
  if (state.pong_stage) lines.push(`    ${pack.onPong}`);
  if (state.pre_stage) lines.push(`    ${pack.preFire}: ${stageSummary(state.pre_stage)}`);
  if (state.post_stage) lines.push(`    ${pack.postFire}: ${stageSummary(state.post_stage)}`);
  if (state.followup_task || state.followup_remind || state.followup_command) {
    lines.push(`    ${pack.ifUnconfirmed}`);
  }
  if (state.preset) lines.push(`    ${pack.preset}: ${state.preset}`);
  return lines.join("\n");
}

function detailLines(state) {
  const pack = L;
  const timerActive = state.scheduler_handle
    ? schedulerIsActive({
        backend: state.scheduler_backend,
        stateDir: STATE_DIR,
        reminderId: state.id,
        schedulerHandle: state.scheduler_handle
      })
    : false;
  const lines = [
    `REMINDER ${state.id}`,
    `kind: ${state.kind === "task" ? pack.kindTask : pack.kindRemind}`,
    `text: ${state.task || state.remind || ""}`,
    `${L.tone}: ${state.tone || "-"}`,
    ,
    `${pack.route}: agent=${state.agent || "-"} channel=${state.channel || "-"} target=${state.target || "-"}`,
    `${pack.schedule}: type=${state.schedule_type} expr=${state.on_calendar || state.schedule_input || "-"}`,
    `${pack.state}: cycle_pokes=${state.cycle_poke_count || 0}/${state.max_pokes === -1 ? "inf" : state.max_pokes} catchup=${state.catchup} confirmed=${state.confirmed ? pack.yes : pack.no}`,
    `${pack.next}: base=${state.next_base_due_at || "-"} poke=${state.next_poke_due_at || "-"} followup=${state.followup_due_at || "-"}`,
    `${pack.tone}: ${state.current_tone || state.tone || "-"}`,
    `${pack.preset}: ${state.preset || "-"}`,
    `${pack.schemaVersion}: ${state.schema_version || "-"}`,
    `${pack.created}: ${state.created_at || "-"}`,
    `${pack.firstDelivered}: ${state.first_delivered_at || "-"}`,
    `${pack.lastDelivered}: ${state.last_delivered || "-"}`,
    `${pack.lastReply}: action=${state.last_reply_action || "-"} at=${state.user_replied_at || "-"}`,
    `${pack.backend}: ${state.scheduler_backend || detectSchedulerBackend()}`,
    `${pack.timer}: ${timerActive ? pack.yes : pack.no}`
  ];
  if (state.pre_stage) lines.push(`pre-fire: ${stageSummary(state.pre_stage)}`);
  if (state.post_stage) lines.push(`post-fire: ${stageSummary(state.post_stage)}`);
  if (state.pong_stage) lines.push(`on-pong: ${stageSummary(state.pong_stage)}`);
  if (state.active_hours) lines.push(`active-hours: ${state.active_hours}`);
  if (state.task_interval) lines.push(`task-interval: ${state.task_interval} (last: ${state.last_task_run_at || "never"})`);
  return lines.join("\n");
}

function parseEscalationIntervals(raw) {
  const values = String(raw || "")
    .split(",")
    .map((entry) => entry.trim())
    .filter(Boolean)
    .map((entry) => Number.parseInt(entry, 10))
    .filter((entry) => Number.isFinite(entry) && entry > 0);
  return values;
}

function toneList(state) {
  return String(state.tones_list || "")
    .split(",")
    .map((entry) => entry.trim())
    .filter(Boolean);
}

async function resolveToneForState(state, runtimeDir) {
  const tones = toneList(state);
  const useVector = state.vector_tones && runtimeDir;
  if (!tones.length && state.tone) {
    return useVector
      ? await resolveToneWithVector(state.tone, state.remind || state.task || "", runtimeDir)
      : resolveToneMetadata(state.tone);
  }
  if (!tones.length) return resolveToneMetadata("default");
  const intervals = parseEscalationIntervals(state.escalation_intervals);
  const deliveryIndex = Math.max((state.cycle_poke_count || 1) - 1, 0);
  let toneIndex = deliveryIndex;
  if (intervals.length > 0) {
    toneIndex = Math.floor((deliveryIndex * tones.length) / intervals.length);
  }
  if (toneIndex >= tones.length) toneIndex = tones.length - 1;
  return resolveToneMetadata(tones[toneIndex]);
}

function nextIntervalSeconds(state, deliveredCount) {
  const intervals = parseEscalationIntervals(state.escalation_intervals);
  if (!intervals.length) return null;
  const index = Math.max(deliveredCount - 1, 0);
  const minutes = intervals[Math.min(index, intervals.length - 1)];
  return minutes * 60;
}

function hasFollowupPayload(state) {
  return Boolean(state.followup_remind || state.followup_task || state.followup_command);
}

function earliestWakeAt(state) {
  const candidates = [state.next_base_due_at, state.next_poke_due_at, state.followup_due_at]
    .filter(Boolean)
    .map((entry) => new Date(entry))
    .filter((entry) => !Number.isNaN(entry.getTime()))
    .sort((left, right) => left.getTime() - right.getTime());
  return candidates[0] || null;
}

function reschedule(state) {
  const nextWake = earliestWakeAt(state);
  if (!nextWake) {
    if (state.scheduler_handle) {
      removeSchedulerWake({
        backend: state.scheduler_backend,
        stateDir: STATE_DIR,
        reminderId: state.id,
        schedulerHandle: state.scheduler_handle
      });
      state.scheduler_handle = null;
      state.scheduler_backend = null;
    }
    return;
  }
  const handle = upsertSchedulerWake({
    backend: state.scheduler_backend || detectSchedulerBackend(),
    stateDir: STATE_DIR,
    reminderId: state.id,
    dueAt: nextWake,
    scriptPath: ENTRY_SCRIPT,
    catchupMode: state.catchup
  });
  state.scheduler_backend = handle.backend;
  state.scheduler_handle = handle;
}

function isTerminal(state) {
  return !state.next_base_due_at && !state.next_poke_due_at && !state.followup_due_at;
}

function finalizeOrPersist(state) {
  if (isTerminal(state)) {
    if (state.scheduler_handle) {
      removeSchedulerWake({
        backend: state.scheduler_backend,
        stateDir: STATE_DIR,
        reminderId: state.id,
        schedulerHandle: state.scheduler_handle
      });
    }
    deleteReminder(state);
    return;
  }
  reschedule(state);
  saveReminder(state);
}

function clearCycleState(state, { preserveReply = false } = {}) {
  state.next_poke_due_at = null;
  state.followup_due_at = null;
  state.followup_fired = false;
  state.followup_fired_at = null;
  state.pong_fired = false;
  state.pong_fired_at = null;
  state.cycle_poke_count = 0;
  // Re-arm pre/post-fire hooks so the next base occurrence runs them again
  // (S1.7 — previously these fired only once per reminder lifetime).
  state.pre_fire_fired = false;
  state.post_fire_fired = false;
  if (!preserveReply) {
    state.user_replied_at = null;
    state.last_reply_action = null;
    state.last_reply_text = null;
  }
}

function queueNextBaseOccurrence(state, afterDate) {
  if (state.schedule_type === "calendar" && state.on_calendar) {
    state.next_base_due_at = nextOccurrenceForCalendar(state.on_calendar, afterDate).toISOString();
  } else {
    state.next_base_due_at = null;
  }
}

function classifyReplyHeuristic(replyText) {
  return classifyReplyIntent(replyText);
}

function classifyReplyWithAgent(agent, replyText, candidates, runtime) {
  const prompt = buildReplyClassifierPrompt(candidates, replyText);
  const raw = runtime.localAgent({ agent, prompt });
  return readJsonFromString(raw) || null;
}

function readJsonFromString(value) {
  try {
    return JSON.parse(String(value || ""));
  } catch {
    return null;
  }
}

function reminderCandidates(channel, target, agent, from = "") {
  return queryReminders({ channel, target, agent })
    .filter((state) => state.last_delivered)
    .filter((state) => !from || state.target === from || state.origin_target === from)
    .slice(0, 5)
    .map((state) => ({
      id: state.id,
      kind: state.kind,
      text: state.task || state.remind || "",
      poke_count: state.cycle_poke_count || 0,
      last_delivered: state.last_delivered || state.created_at || "",
      user_replied_at: state.user_replied_at || ""
    }));
}

function parseCatchupMode(value) {
  const mode = String(value || "").trim().toLowerCase();
  if (!["none", "coalesce", "replay"].includes(mode)) {
    throw new Error(`Invalid catchup mode '${value}' — use coalesce or replay`);
  }
  return mode;
}

function nextDueBaseOccurrences(state, now) {
  if (!state.next_base_due_at) return [];
  const nextBase = new Date(state.next_base_due_at);
  if (Number.isNaN(nextBase.getTime()) || nextBase.getTime() > now.getTime()) return [];
  if (state.schedule_type === "calendar" && state.on_calendar) {
    const cursor = state.last_processed_occurrence ? new Date(state.last_processed_occurrence) : new Date(state.created_at);
    const due = occurrencesBetween(state.on_calendar, cursor, now, Math.max(state.max_catchup_runs || DEFAULT_MAX_CATCHUP_RUNS, 64));
    if (!due.length) return [];
    if (state.catchup === "replay") return due.slice(0, state.max_catchup_runs || DEFAULT_MAX_CATCHUP_RUNS);
    return [due[due.length - 1]];
  }
  return [nextBase];
}

function nextDuePokeOccurrences(state, now) {
  if (!state.next_poke_due_at) return [];
  let nextAt = new Date(state.next_poke_due_at);
  if (Number.isNaN(nextAt.getTime()) || nextAt.getTime() > now.getTime()) return [];
  const due = [];
  let simulatedCount = state.cycle_poke_count || 0;
  const limit = state.catchup === "replay" ? state.max_catchup_runs || DEFAULT_MAX_CATCHUP_RUNS : 64;
  while (due.length < limit && nextAt.getTime() <= now.getTime()) {
    due.push(new Date(nextAt));
    simulatedCount += 1;
    if (state.max_pokes !== -1 && simulatedCount >= state.max_pokes) break;
    const intervalSeconds = nextIntervalSeconds(state, simulatedCount);
    if (!intervalSeconds) break;
    nextAt = new Date(nextAt.getTime() + intervalSeconds * 1000);
  }
  if (state.catchup === "replay") return due;
  return due.length ? [due[due.length - 1]] : [];
}

function maybeResetReplyCycle(state) {
  if ((state.cycle_poke_count || 0) === 0) {
    state.user_replied_at = null;
    state.last_reply_action = null;
    state.last_reply_text = null;
    state.followup_due_at = null;
    state.followup_fired = false;
    state.followup_fired_at = null;
    state.pong_fired = false;
    state.pong_fired_at = null;
  }
}

function buildTaskPayload(state, tone) {
  const count = (state.cycle_poke_count || 0) + 1;
  const prefix = L.taskPrefix(count);
  const directive = buildToneDirective(tone);
  const commitmentContext = buildCommitmentContextForPrompt();
  return [prefix, "", state.task, commitmentContext, directive ? `\n${directive}` : ""].filter(Boolean).join("\n");
}

// A reminder is delivered BY the agent (LLM), never as a static string. We hand
// the agent the canonical intent + tone directive and let it phrase + deliver in
// the intent's own language. Variation/escalation is the agent's job, guided here.
function buildReminderDeliveryPrompt(state, tone) {
  const count = (state.cycle_poke_count || 0) + 1;
  const directive = buildToneDirective(tone);
  return [
    "Deliver this reminder to the user now, on this channel. Phrase it naturally in your own words — do not echo the intent verbatim — and reply in the same language the intent is written in.",
    count > 1 ? `This is reminder #${count}; they haven't acknowledged yet, so make it land with a bit more urgency than before.` : "",
    directive,
    "",
    `Reminder intent: ${String(state.remind || "").trim()}`
  ].filter(Boolean).join("\n");
}

async function buildPrimaryDeliveryAction(state, runtime) {
  const tone = await resolveToneForState(state, STATE_DIR);
  state.current_tone = tone?.data?.id || tone?.data?.name || state.current_tone || state.tone || null;
  const prompt = state.kind === "task" ? buildTaskPayload(state, tone) : buildReminderDeliveryPrompt(state, tone);
  return { type: "agent_deliver", prompt };
}

function buildFollowupAction(state) {
  if (state.followup_command) {
    return { type: "hook", hookName: "no-pong", command: state.followup_command };
  }
  if (state.followup_task) {
    return { type: "agent_deliver", prompt: `${L.followupTaskPrefix}\n\n${state.followup_task}` };
  }
  if (state.followup_remind) {
    return {
      type: "agent_deliver",
      prompt: `Deliver this follow-up reminder to the user now, phrased naturally in the intent's language:\n\n${state.followup_remind}`
    };
  }
  return null;
}

// Every delivery goes through the agent (runtime.deliver → `agent --local --deliver`).
// Poke NEVER sends a static message and NEVER inspects the reply (no HEARTBEAT_OK /
// dedup — those are OpenClaw's job or unnecessary). Only flag-level gates apply.
function dispatchDeliveryAction(state, runtime, action) {
  if (!action) return;
  const channels = (state.channel || "").split(",").map((s) => s.trim()).filter(Boolean);
  const targets = (state.target || "").split(",").map((s) => s.trim()).filter(Boolean);
  const pairs = [];
  if (channels.length && targets.length) {
    for (const ch of channels) for (const tgt of targets) pairs.push({ channel: ch, target: tgt });
  } else if (channels.length) {
    for (const ch of channels) pairs.push({ channel: ch, target: state.target });
  } else {
    pairs.push({ channel: state.channel, target: state.target });
  }
  for (const { channel, target } of pairs) {
    if (action.type === "agent_deliver") {
      if (!shouldDeliver(state)) {
        appendHistory({ event: "suppressed", id: state.id, channel, target, reason: "gate" });
        continue;
      }
      const agent = state.agent || runtime.defaultAgentId();
      runtime.deliver({ agent, channel, target, prompt: action.prompt, sessionHint: target || channel });
      if (state.task_interval) state.last_task_run_at = new Date().toISOString();
      appendHistory({
        event: "delivered",
        id: state.id,
        kind: state.kind,
        channel,
        target,
        cycle_poke_count: state.cycle_poke_count || 0
      });
    } else {
      throw new Error(`Unsupported delivery action: ${action.type}`);
    }
  }
}

function startFollowupTimer(state, deliveredAt) {
  if (state.followup_after_seconds && !state.user_replied_at && !state.followup_due_at && hasFollowupPayload(state)) {
    state.followup_due_at = new Date(deliveredAt.getTime() + state.followup_after_seconds * 1000).toISOString();
  }
}

function postDeliveryScheduling(state, deliveredAt) {
  const deliveredCount = state.cycle_poke_count;
  const shouldStopPokes = state.max_pokes !== -1 && deliveredCount >= state.max_pokes;
  if (shouldStopPokes) {
    state.next_poke_due_at = null;
    return;
  }

  const intervalSeconds = nextIntervalSeconds(state, deliveredCount);
  if (!intervalSeconds) {
    state.next_poke_due_at = null;
    return;
  }

  const nextAt = new Date(deliveredAt.getTime() + intervalSeconds * 1000);
  if (state.followup_after_pokes && hasFollowupPayload(state) && deliveredCount >= state.followup_after_pokes) {
    state.next_poke_due_at = null;
    state.followup_due_at = nextAt.toISOString();
    return;
  }
  state.next_poke_due_at = nextAt.toISOString();
}

function applyDeliveryMutation(state, occurrenceDate) {
  maybeResetReplyCycle(state);
  state.cycle_poke_count = (state.cycle_poke_count || 0) + 1;
  state.poke_count = (state.poke_count || 0) + 1;
  state.last_delivered = occurrenceDate.toISOString();
  state.first_delivered_at = state.first_delivered_at || occurrenceDate.toISOString();
  state.last_processed_occurrence = occurrenceDate.toISOString();
  queueNextBaseOccurrence(state, occurrenceDate);
  startFollowupTimer(state, occurrenceDate);
  postDeliveryScheduling(state, occurrenceDate);
}

async function maybeWaitUntilDue(state) {
  const nextWake = earliestWakeAt(state);
  if (!nextWake) return;
  const now = Date.now();
  const delta = nextWake.getTime() - now;
  if (delta > 0 && delta <= 65_000) {
    await new Promise((resolve) => setTimeout(resolve, delta));
  }
}

function rotateRecurringCycleIfIdle(state) {
  if (state.next_base_due_at) return;
  if (state.schedule_type !== "calendar") return;
  clearCycleState(state);
  queueNextBaseOccurrence(state, new Date());
}

function fireFollowup(state, runtime) {
  if (state.user_replied_at || !hasFollowupPayload(state)) return false;
  dispatchDeliveryAction(state, runtime, buildFollowupAction(state));
  state.followup_fired = true;
  state.followup_fired_at = new Date().toISOString();
  state.followup_due_at = null;
  state.next_poke_due_at = null;
  // Audit trail — important for once-mode reminders that terminate right
  // after this and otherwise leave no trace the followup ever fired.
  appendHistory({
    event: "followup_fired",
    id: state.id,
    schedule_type: state.schedule_type
  });
  if (state.schedule_type === "calendar") {
    clearCycleState(state);
    if (!state.next_base_due_at) queueNextBaseOccurrence(state, new Date());
    return true;
  }
  state.next_base_due_at = null;
  return true;
}

function maybeRunPongCommand(state, replyAction) {
  if (!state.pong_stage || state.pong_fired) return;
  runHookStage(state, "pong", state.pong_stage, null, replyAction);
  state.pong_fired = true;
  state.pong_fired_at = new Date().toISOString();
}

function isQuietHours(quietHoursStr, now) {
  if (!quietHoursStr) return false;
  const parts = quietHoursStr.split("-");
  if (parts.length !== 2) return false;
  const [startStr, endStr] = parts;
  const [startH, startM] = startStr.split(":").map(Number);
  const [endH, endM] = endStr.split(":").map(Number);
  if (isNaN(startH) || isNaN(endH)) return false;
  const mins = now.getHours() * 60 + now.getMinutes();
  const start = startH * 60 + (startM || 0);
  const end = endH * 60 + (endM || 0);
  if (start <= end) return mins >= start && mins < end;
  return mins >= start || mins < end; // wraps midnight
}

function isActiveHours(activeHoursStr, now) {
  if (!activeHoursStr) return true; // no restriction = always active
  return !isQuietHours(activeHoursStr, now); // active hours is the inverse of quiet hours
}

// ── Flood Guard ──────────────────────────────────────────────────────
// Prevents rapid-fire delivery. Tracks global delivery timestamps.
// Default: max 5 deliveries per 60-second window.

const FLOOD_WINDOW_MS = 60_000;
const FLOOD_THRESHOLD = 5;

function loadFloodState() {
  return readJson(FLOOD_FILE, { recent_deliveries: [] });
}

function saveFloodState(state) {
  ensureDirectory(STATE_DIR);
  writeJson(FLOOD_FILE, state);
}

function isFloodBlocked() {
  const state = loadFloodState();
  const now = Date.now();
  const windowStart = now - FLOOD_WINDOW_MS;
  // Prune old entries
  state.recent_deliveries = (state.recent_deliveries || []).filter((ts) => ts > windowStart);
  saveFloodState(state);
  return state.recent_deliveries.length >= FLOOD_THRESHOLD;
}

function recordDelivery() {
  const state = loadFloodState();
  const now = Date.now();
  const windowStart = now - FLOOD_WINDOW_MS;
  state.recent_deliveries = (state.recent_deliveries || []).filter((ts) => ts > windowStart);
  state.recent_deliveries.push(now);
  saveFloodState(state);
}

// ── Busy Lane Detection ──────────────────────────────────────────────
// Checks if OpenClaw has active agent sessions/lane work queued.
// Returns true if the system appears busy (cron, subagents, etc.).

const BUSY_LANE_KINDS = new Set(["cron", "subagent", "lane"]);

function isBusyLane(runtime) {
  try {
    const storePath = path.join(runtime.stateDir, "sessions.json");
    const store = readJson(storePath, null);
    if (!store || typeof store !== "object") return false;
    const now = Date.now();
    const BUSY_THRESHOLD_MS = 120_000; // 2 minutes
    // Check for recently active sessions whose entry.kind marks them as lane work.
    // We match against a structured `kind` field — substring matching on the key
    // is unreliable (S2.5).
    for (const entry of Object.values(store)) {
      if (!entry || typeof entry !== "object") continue;
      const lastActive = entry.lastActivityAt || entry.sessionStartedAt || 0;
      if (lastActive && now - lastActive < BUSY_THRESHOLD_MS) {
        const kind = typeof entry.kind === "string" ? entry.kind.toLowerCase() : "";
        if (BUSY_LANE_KINDS.has(kind)) return true;
      }
    }
    return false;
  } catch {
    return false;
  }
}

// ── Visibility Controls ──────────────────────────────────────────────
// Per-channel settings for what gets delivered.
// Modes: "all" (default), "urgent" (only reminders marked --urgent)

function loadVisibility() {
  return readJson(VISIBILITY_FILE, { channels: {} });
}

function getChannelVisibility(channel) {
  const vis = loadVisibility();
  return vis.channels?.[channel] || "all";
}

function shouldDeliver(state) {
  if (state.urgent) return true;
  const channels = (state.channel || "").split(",").map((s) => s.trim()).filter(Boolean);
  for (const ch of channels) {
    if (getChannelVisibility(ch) === "urgent") return false;
  }
  return true;
}

// ── Commitments ──────────────────────────────────────────────────────
// Inferred follow-up promises from conversations.
// "I'll check on that tomorrow" → auto-scheduled commitment.

const COMMITMENT_KINDS = ["event_check_in", "deadline_check", "care_check_in", "open_loop"];
const COMMITMENT_SENSITIVITIES = ["routine", "personal", "care"];

function loadCommitments() {
  const data = readJson(COMMITMENTS_FILE, { version: 1, commitments: [] });
  if (!data.commitments) data.commitments = [];
  return data;
}

function saveCommitments(store) {
  ensureDirectory(STATE_DIR);
  writeJson(COMMITMENTS_FILE, store);
}

function generateCommitmentId() {
  const now = new Date();
  const ts = [now.getFullYear(), String(now.getMonth()+1).padStart(2,"0"), String(now.getDate()).padStart(2,"0")].join("");
  const clock = [String(now.getHours()).padStart(2,"0"), String(now.getMinutes()).padStart(2,"0"), String(now.getSeconds()).padStart(2,"0")].join("");
  const rand = Math.random().toString(16).slice(2,10);
  return `cm-${ts}-${clock}-${rand}`;
}

function createCommitment({ reason, suggestedText, dueEarliest, dueLatest, kind, sensitivity, channel, target, agent }) {
  const now = Date.now();
  const store = loadCommitments();
  const commitment = {
    id: generateCommitmentId(),
    agent: agent || "",
    channel: channel || "",
    target: target || "",
    kind: kind || "open_loop",
    sensitivity: sensitivity || "routine",
    source: "agent_promise",
    status: "pending",
    reason: reason || "",
    suggestedText: suggestedText || reason || "",
    confidence: 0.8,
    dueWindow: {
      earliestMs: dueEarliest || now,
      latestMs: dueLatest || dueEarliest || now + 86400000,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC"
    },
    dedupeKey: createHash("sha256").update(`${reason}:${dueEarliest}`).digest("hex").slice(0, 16),
    createdAtMs: now,
    updatedAtMs: now,
    attempts: 0
  };
  store.commitments.push(commitment);
  saveCommitments(store);
  return commitment;
}

function listDueCommitments(nowMs) {
  const store = loadCommitments();
  const now = nowMs || Date.now();
  return store.commitments.filter(c => 
    c.status === "pending" && 
    c.dueWindow.earliestMs <= now &&
    (!c.dueWindow.latestMs || c.dueWindow.latestMs >= now - 86400000) // within 24h of latest
  );
}

function completeCommitment(id) {
  const store = loadCommitments();
  const c = store.commitments.find(c => c.id === id);
  if (!c) throw new Error(`Commitment not found: ${id}`);
  c.status = "completed";
  c.updatedAtMs = Date.now();
  saveCommitments(store);
  return c;
}

function cancelCommitment(id) {
  const store = loadCommitments();
  const c = store.commitments.find(c => c.id === id);
  if (!c) throw new Error(`Commitment not found: ${id}`);
  c.status = "cancelled";
  c.updatedAtMs = Date.now();
  saveCommitments(store);
  return c;
}

function expireStaleCommitments() {
  const store = loadCommitments();
  const now = Date.now();
  const STALE_MS = 7 * 86400000; // 7 days
  let changed = false;
  for (const c of store.commitments) {
    if (c.status === "pending" && c.dueWindow.latestMs + STALE_MS < now) {
      c.status = "expired";
      c.updatedAtMs = now;
      changed = true;
    }
  }
  if (changed) saveCommitments(store);
}

function formatCommitmentBrief(c) {
  const dueDate = new Date(c.dueWindow.earliestMs);
  const now = new Date();
  const isToday = dueDate.toDateString() === now.toDateString();
  const timeStr = dueDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  const dateStr = isToday ? "today" : dueDate.toLocaleDateString();
  return `${c.id} [${c.kind}] ${c.reason} — due ${dateStr} ${timeStr}`;
}

function buildCommitmentContextForPrompt() {
  expireStaleCommitments();
  const due = listDueCommitments();
  if (!due.length) return "";
  const lines = due.map(c => `- ${c.reason} (due: ${new Date(c.dueWindow.earliestMs).toLocaleString()}, suggested: "${c.suggestedText}")`);
  return `\n\nDue follow-up commitments:\n${lines.join("\n")}\nConsider addressing these. If any are no longer relevant, they can be ignored.`;
}

function isTaskIntervalDue(state, now) {
  if (!state.task_interval) return true; // no interval = always due
  if (!state.last_task_run_at) return true; // never run = due
  try {
    const intervalMs = parseDuration(state.task_interval) * 1000;
    return now.getTime() - new Date(state.last_task_run_at).getTime() >= intervalMs;
  } catch {
    return true;
  }
}

async function handleDeliver(id) {
  const state = loadReminder(id);
  if (!state) {
    removeSchedulerWake({ stateDir: STATE_DIR, reminderId: id });
    return 0;
  }

  await maybeWaitUntilDue(state);
  const runtime = loadRuntime();
  const now = nowDate();

  // Check snooze
  if (state.snooze_until && new Date(state.snooze_until).getTime() > now.getTime()) {
    // Snoozed — reschedule for after snooze expires
    state.next_poke_due_at = state.snooze_until;
    reschedule(state);
    saveReminder(state);
    return 0;
  }
  state.snooze_until = null;

  // Check DND (urgent reminders bypass)
  if (!state.urgent && isDndActive(now)) {
    const dnd = loadDnd();
    if (dnd?.until) {
      state.next_poke_due_at = dnd.until;
      reschedule(state);
      saveReminder(state);
      return 0;
    }
    // No expiry — just skip this fire, will retry on next wake
    reschedule(state);
    saveReminder(state);
    return 0;
  }

  // Check quiet hours (urgent reminders bypass). Per-reminder only —
  // the global default mechanism was removed.
  const quietWindow = effectiveQuietHours(state);
  if (!state.urgent && isQuietHours(quietWindow, now)) {
    // In quiet hours — delay until end of quiet window
    const parts = quietWindow.split("-");
    const [endH, endM] = parts[1].split(":").map(Number);
    const end = new Date(now);
    end.setHours(endH, endM || 0, 0, 0);
    if (end <= now) end.setDate(end.getDate() + 1);
    state.next_poke_due_at = end.toISOString();
    reschedule(state);
    saveReminder(state);
    return 0;
  }

  // Check active hours (urgent reminders bypass)
  // Active hours is the inverse of quiet hours — only deliver WITHIN this window
  if (!state.urgent && !isActiveHours(state.active_hours, now)) {
    // Outside active hours — delay until start of active window
    const parts = state.active_hours.split("-");
    const [startH, startM] = parts[0].split(":").map(Number);
    const start = new Date(now);
    start.setHours(startH, startM || 0, 0, 0);
    if (start <= now) start.setDate(start.getDate() + 1);
    state.next_poke_due_at = start.toISOString();
    reschedule(state);
    saveReminder(state);
    return 0;
  }

  // Flood guard — too many deliveries in the window
  if (!state.urgent && isFloodBlocked()) {
    // Defer by 30s and retry
    state.next_poke_due_at = new Date(now.getTime() + 30_000).toISOString();
    reschedule(state);
    saveReminder(state);
    return 0;
  }

  // Busy lane detection — system has active work queued
  if (!state.urgent && isBusyLane(runtime)) {
    // Defer by 60s and retry
    state.next_poke_due_at = new Date(now.getTime() + 60_000).toISOString();
    reschedule(state);
    saveReminder(state);
    return 0;
  }

  // Check task interval
  if (!isTaskIntervalDue(state, now)) {
    // Not due yet — reschedule for when interval elapses
    const intervalMs = parseDuration(state.task_interval) * 1000;
    const nextDue = new Date(new Date(state.last_task_run_at).getTime() + intervalMs);
    state.next_poke_due_at = nextDue.toISOString();
    reschedule(state);
    saveReminder(state);
    return 0;
  }

  // Check dependencies
  if (state.depends_on) {
    const depIds = state.depends_on.split(",").map(s => s.trim()).filter(Boolean);
    const unresolved = depIds.filter(id => {
      const dep = loadReminder(id);
      return dep && !dep.confirmed && !dep.cancelled;
    });
    if (unresolved.length) {
      // Dependencies not met — reschedule for later
      state.next_poke_due_at = new Date(now.getTime() + 60000).toISOString();
      reschedule(state);
      saveReminder(state);
      return 0;
    }
    // All resolved — clear dependency
    state.depends_on = null;
  }

  if (state.followup_due_at && new Date(state.followup_due_at).getTime() <= now.getTime() && !state.user_replied_at) {
    fireFollowup(state, runtime);
    finalizeOrPersist(state);
    return 0;
  }

  const duePokes = nextDuePokeOccurrences(state, now);
  if (duePokes.length) {
    if (state.pre_stage && !state.pre_fire_fired) {
      runHookStage(state, "pre-fire", state.pre_stage, runtime);
      state.pre_fire_fired = true;
    }
    for (const occurrence of duePokes) {
      dispatchDeliveryAction(state, runtime, await buildPrimaryDeliveryAction(state, runtime));
      applyDeliveryMutation(state, occurrence);
      if (state.catchup !== "replay") break;
    }
    if (state.post_stage && !state.post_fire_fired) {
      runHookStage(state, "post-fire", state.post_stage, runtime);
      state.post_fire_fired = true;
    }
    recordDelivery();
    finalizeOrPersist(state);
    return 0;
  }

  const dueBase = nextDueBaseOccurrences(state, now);
  if (dueBase.length) {
    if (state.pre_stage && !state.pre_fire_fired) {
      runHookStage(state, "pre-fire", state.pre_stage, runtime);
      state.pre_fire_fired = true;
    }
    for (const occurrence of dueBase) {
      dispatchDeliveryAction(state, runtime, await buildPrimaryDeliveryAction(state, runtime));
      applyDeliveryMutation(state, occurrence);
      if (state.catchup !== "replay") break;
    }
    if (state.post_stage && !state.post_fire_fired) {
      runHookStage(state, "post-fire", state.post_stage, runtime);
      state.post_fire_fired = true;
    }
    recordDelivery();
    finalizeOrPersist(state);
    return 0;
  }

  rotateRecurringCycleIfIdle(state);
  finalizeOrPersist(state);
  return 0;
}

function buildCreateState(options) {
  // S2.6: validate --depends-on IDs exist at create time. (Missing-at-fire is
  // still treated as resolved-by-deletion — that path is for legitimately
  // confirmed/cancelled deps that got cleaned up.)
  if (options.dependsOn) {
    const depIds = String(options.dependsOn).split(",").map((s) => s.trim()).filter(Boolean);
    const missing = depIds.filter((id) => !loadReminder(id));
    if (missing.length) {
      throw new Error(`--depends-on references unknown reminder id(s): ${missing.join(", ")}`);
    }
  }

  const now = new Date();
  const kind = options.taskPrompt ? "task" : "remind";
  const expandedTask = options.taskPrompt ? expandPathPlaceholders(options.taskPrompt) : "";
  const expandedRemind = options.remindText ? expandPathPlaceholders(options.remindText) : "";

  const state = {
    schema_version: 5,
    id: generateId(),
    kind,
    task: expandedTask || null,
    remind: expandedRemind || null,
    agent: options.agent || "",
    channel: options.channel,
    target: options.target,
    schedule_type: options.mode === "calendar" ? "calendar" : "once",
    schedule_input: options.onceDelay || options.atTime || options.onCalendar || "",
    on_calendar: options.onCalendar || null,
    catchup: parseCatchupMode(options.catchupMode),
    max_catchup_runs: options.maxCatchupRuns || DEFAULT_MAX_CATCHUP_RUNS,
    max_pokes: options.maxPokes ? Number.parseInt(options.maxPokes, 10) : options.mode === "calendar" ? -1 : 1,
    tone:
      options.toneRaw && !options.toneRaw.includes(",")
        ? resolveToneMetadata(options.toneRaw)?.data?.id || options.toneRaw
        : null,
    tones_list: options.toneRaw && options.toneRaw.includes(",") ? options.toneRaw : null,
    escalation_intervals: options.escalationIntervals || null,
    current_tone: null,
    escalation_index: 0,
    poke_count: 0,
    cycle_poke_count: 0,
    next_base_due_at: null,
    next_poke_due_at: null,
    followup_due_at: null,
    followup_after_seconds: options.followupAfter ? parseDuration(options.followupAfter) : null,
    followup_after_pokes: options.followupAfterPokes ? Number.parseInt(options.followupAfterPokes, 10) : null,
    followup_remind: options.followupRemind || null,
    followup_task: options.followupTask || null,
    followup_command: options.followupCommand || null,
    followup_fired: false,
    followup_fired_at: null,
    pre_stage: options.preStage || null,
    post_stage: options.postStage || null,
    pong_stage: options.pongStage || null,
    hook_env: options.hookEnv.length ? options.hookEnv : null,
    pong_fired: false,
    pong_fired_at: null,
    pre_fire_fired: false,
    post_fire_fired: false,
    // Snapshot of the channel/target the reminder was scheduled against, so
    // an agent-prompt stage (--pre-task / --post-task) can deliver "back to
    // where this was scheduled from" without re-specifying it.
    origin_channel: options.channel || "",
    origin_target: options.target || "",
    active_hours: options.activeHours || null,
    task_interval: options.taskInterval || null,
    last_task_run_at: null,
    user_replied_at: null,
    last_reply_action: null,
    snooze_until: null,
    quiet_hours: options.quietHours || null,
    depends_on: options.dependsOn || null,
    urgent: options.urgent || false,
    last_reply_text: null,
    first_delivered_at: null,
    last_delivered: null,
    last_processed_occurrence: null,
    preset: options.presetName,
    preset_file: options.presetFile,
    created_at: now.toISOString(),
    confirmed: false,
    cancelled: false,
    scheduler_backend: detectSchedulerBackend(),
    vector_tones: options.vectorTones || false,
    scheduler_handle: null
  };

  if (options.mode === "once") {
    state.next_base_due_at = new Date(now.getTime() + parseDuration(options.onceDelay) * 1000).toISOString();
  } else if (options.mode === "at") {
    state.next_base_due_at = parseAtInput(options.atTime).toISOString();
  } else if (options.mode === "calendar") {
    parseOnCalendarExpression(options.onCalendar);
    state.next_base_due_at = nextOccurrenceForCalendar(options.onCalendar, now).toISOString();
  } else {
    throw new Error("Need schedule (--once, --at, --on-calendar, or preset)");
  }

  return state;
}

function printHelp() {
  process.stdout.write(L.helpText);
}

function printAvailableTones() {
  const pack = L;
  process.stdout.write(`${pack.availableTones}\n`);
  for (const tone of loadToneFiles()) {
    process.stdout.write(`  ${tone.data.id || "?"}\n`);
    process.stdout.write(`    ${tone.data.description || pack.noDescription}\n\n`);
  }
}

function printAvailablePresets() {
  const pack = L;
  process.stdout.write(`${pack.availablePresets}\n`);
  const loadDir = PRESETS_DIR;
  for (const entry of fs.readdirSync(loadDir).filter((name) => name.endsWith(".json")).sort()) {
    const preset = readJson(path.join(loadDir, entry), {});
    process.stdout.write(`  ${preset.id || entry.replace(/\.json$/, "")}\n`);
    process.stdout.write(
      `    ${preset.description || ""} | ${pack.tone}: ${preset.tone || pack.none} | ${pack.task}: ${preset.task ? pack.taskYes : pack.taskNo}\n`
    );
    process.stdout.write(`    ${pack.schedule}: ${preset.schedule?.on_calendar || pack.none}\n\n`);
  }
}

async function handleReply(options) {
  if (!options.channel) throw new Error("--channel is required for --reply");
  if (!options.target) throw new Error("--target is required for --reply");
  if (options.replyText === "@stdin") {
    options.replyText = fs.readFileSync(0, "utf8").trim();
  }

  const runtime = loadRuntime();
  let agent = options.agent || runtime.defaultAgentId();
  const candidates = reminderCandidates(options.channel, options.target, agent, options.from);
  if (!candidates.length) {
    process.stdout.write("REPLY no_match\n");
    return 0;
  }

  let matchId = "";
  let replyAction = "";
  if (candidates.length === 1) {
    const heuristic = classifyReplyHeuristic(options.replyText);
    if (heuristic !== "ignore") {
      matchId = candidates[0].id;
      replyAction = heuristic;
    }
  }

  if (!replyAction && agent) {
    const classified = classifyReplyWithAgent(agent, options.replyText, candidates, runtime);
    if (classified?.match_id && classified?.action && classified.match_id !== "none" && classified.action !== "ignore") {
      matchId = classified.match_id;
      replyAction = classified.action;
    }
  }

  if (!replyAction) {
    process.stdout.write("REPLY no_match\n");
    return 0;
  }

  const state = loadReminder(matchId);
  if (!state) {
    process.stdout.write("REPLY no_match\n");
    return 0;
  }

  state.user_replied_at = new Date().toISOString();
  state.last_reply_action = replyAction;
  state.last_reply_text = options.replyText;

  if (replyAction === "cancel") {
    maybeRunPongCommand(state, "cancel");
    state.cancelled = true;
    state.next_base_due_at = null;
    state.next_poke_due_at = null;
    state.followup_due_at = null;
    finalizeOrPersist(state);
    appendHistory({ event: "cancel", id: matchId, schedule_type: state.schedule_type });
    process.stdout.write(`REPLY matched id=${matchId} action=cancel\n`);
    return 0;
  }

  if (replyAction === "confirm") {
    maybeRunPongCommand(state, "confirm");
    state.next_poke_due_at = null;
    state.followup_due_at = null;
    if (state.schedule_type === "calendar") {
      // Recurring: this iteration is done; advance to next occurrence.
      // Mirrors the followup branch but records action=confirm.
      clearCycleState(state, { preserveReply: true });
      if (!state.next_base_due_at) queueNextBaseOccurrence(state, new Date());
      reschedule(state);
      saveReminder(state);
    } else {
      // One-off: mark confirmed and terminate.
      state.confirmed = true;
      state.next_base_due_at = null;
      finalizeOrPersist(state);
    }
    appendHistory({ event: "confirm", id: matchId, schedule_type: state.schedule_type });
    process.stdout.write(`REPLY matched id=${matchId} action=confirm\n`);
    return 0;
  }

  if (replyAction === "snooze") {
    const snoozeSec = parseSnoozeDuration(options.replyText);
    const snoozeUntil = new Date(Date.now() + snoozeSec * 1000).toISOString();
    state.snooze_until = snoozeUntil;
    state.next_poke_due_at = null;
    state.followup_due_at = null;
    state.cycle_poke_count = Math.max((state.cycle_poke_count || 1) - 1, 0);
    reschedule(state);
    saveReminder(state);
    appendHistory({ event: "snooze", id: matchId, until: snoozeUntil, seconds: snoozeSec });
    process.stdout.write(`REPLY matched id=${matchId} action=snooze until=${snoozeUntil}\n`);
    return 0;
  }

  maybeRunPongCommand(state, replyAction);
  state.next_poke_due_at = null;
  state.followup_due_at = null;
  if (state.schedule_type === "calendar") {
    clearCycleState(state, { preserveReply: true });
    if (!state.next_base_due_at) queueNextBaseOccurrence(state, new Date());
    reschedule(state);
    saveReminder(state);
  } else {
    state.next_base_due_at = null;
    finalizeOrPersist(state);
  }
  appendHistory({ event: replyAction, id: matchId, schedule_type: state.schedule_type });
  process.stdout.write(`REPLY matched id=${matchId} action=${replyAction}\n`);
  return 0;
}

export async function main(argv) {
  ensureStateDir();
  try {
    const options = parseArgs(argv);
    applyPresets(options);

    switch (options.mode) {
      case "help":
      case "":
        printHelp();
        return 0;
      case "tones":
        printAvailableTones();
        return 0;
      case "presets":
        printAvailablePresets();
        return 0;
      case "paths-list": {
        const pack = L;
        process.stdout.write(`${pack.savedPathSets}\n`);
        const entries = listPathSets();
        if (!entries.length) {
          process.stdout.write(`  ${pack.none}\n`);
          return 0;
        }
        for (const [name, entry] of entries) {
          process.stdout.write(`  ${name}\n`);
          process.stdout.write(`    ${pack.files}: ${(entry.files || []).length} | ${pack.updated}: ${entry.updated_at || pack.unknown}\n`);
        }
        return 0;
      }
      case "paths-show": {
        const entry = showPathSet(options.pathSetName);
        if (!entry) throw new Error(`No saved path set: ${options.pathSetName}`);
        process.stdout.write(`PATH_SET ${options.pathSetName} files=${entry.files.length}\n`);
        for (const filePath of entry.files) process.stdout.write(`- ${filePath}\n`);
        return 0;
      }
      case "paths-save":
        savePathSet(options.pathSetName, options.pathFiles);
        process.stdout.write(`${L.pathSetSaved(options.pathSetName, options.pathFiles.length)}\n`);
        return 0;
      case "paths-delete":
        deletePathSet(options.pathSetName);
        process.stdout.write(`${L.pathSetDeleted(options.pathSetName)}\n`);
        return 0;
      case "list": {
        const pack = L;
        const reminders = queryReminders({ channel: options.channel, target: options.target, agent: options.agent });
        process.stdout.write(`${pack.activeReminders}\n`);
        if (!reminders.length) {
          process.stdout.write(`  ${pack.none}\n`);
          return 0;
        }
        for (const state of reminders) process.stdout.write(`${summaryLine(state)}\n\n`);
        return 0;
      }
      case "latest": {
        const reminders = queryReminders({ channel: options.channel, target: options.target, agent: options.agent });
        if (!reminders.length) {
          process.stdout.write("LATEST none\n");
          return 0;
        }
        process.stdout.write(`${detailLines(reminders[0])}\n`);
        return 0;
      }
      case "show": {
        const state = loadReminder(options.id);
        if (!state) throw new Error(`No reminder: ${options.id}`);
        process.stdout.write(`${detailLines(state)}\n`);
        return 0;
      }
      case "confirm": {
        const state = loadReminder(options.id);
        if (!state) throw new Error(`No reminder: ${options.id}`);
        state.confirmed = true;
        state.next_base_due_at = null;
        state.next_poke_due_at = null;
        state.followup_due_at = null;
        finalizeOrPersist(state);
        appendHistory({ event: "confirm", id: options.id, source: "cli" });
        process.stdout.write(`${L.confirmed(options.id)}\n`);
        return 0;
      }
      case "cancel": {
        const state = loadReminder(options.id);
        if (!state) throw new Error(`No reminder: ${options.id}`);
        state.cancelled = true;
        state.next_base_due_at = null;
        state.next_poke_due_at = null;
        state.followup_due_at = null;
        finalizeOrPersist(state);
        appendHistory({ event: "cancel", id: options.id, source: "cli" });
        process.stdout.write(`${L.cancelled(options.id)}\n`);
        return 0;
      }
      case "cancel-all": {
        const pack = L;
        let count = 0;
        for (const state of queryReminders()) {
          state.cancelled = true;
          state.next_base_due_at = null;
          state.next_poke_due_at = null;
          state.followup_due_at = null;
          finalizeOrPersist(state);
          appendHistory({ event: "cancel", id: state.id, source: "cancel-all" });
          count += 1;
        }
        process.stdout.write(`${pack.cancelledAll(count)}\n`);
        return 0;
      }
      case "dnd": {
        process.stdout.write(`${dndStatusText()}\n`);
        return 0;
      }
      case "dnd-on": {
        const until = parseDndDuration(options.dndUntil);
        saveDnd({ until, enabled_at: new Date().toISOString() });
        process.stdout.write(`DND enabled until ${new Date(until).toLocaleTimeString()}\n`);
        return 0;
      }
      case "dnd-off": {
        saveDnd(null);
        process.stdout.write("DND disabled.\n");
        return 0;
      }
      case "visibility": {
        const vis = loadVisibility();
        const channels = vis.channels || {};
        const entries = Object.entries(channels);
        if (!entries.length) {
          process.stdout.write("Visibility: all channels default to 'all'\n");
        } else {
          process.stdout.write("Visibility settings:\n");
          for (const [ch, mode] of entries) {
            process.stdout.write(`  ${ch}: ${mode}\n`);
          }
        }
        return 0;
      }
      case "visibility-set": {
        if (!options.visibilityChannel || !options.visibilityMode) {
          throw new Error("Usage: --visibility-set CHANNEL MODE (all/alerts/urgent)");
        }
        const validModes = ["all", "urgent"];
        if (!validModes.includes(options.visibilityMode)) {
          throw new Error(`Invalid visibility mode '${options.visibilityMode}'. Use: all, urgent`);
        }
        const vis = loadVisibility();
        if (!vis.channels) vis.channels = {};
        vis.channels[options.visibilityChannel] = options.visibilityMode;
        ensureDirectory(STATE_DIR);
        writeJson(VISIBILITY_FILE, vis);
        process.stdout.write(`Visibility: ${options.visibilityChannel} = ${options.visibilityMode}\n`);
        return 0;
      }
      case "commit": {
        if (!options.commitReason) throw new Error("--commit requires a reason");
        const dueMs = options.commitDue ? parseDuration(options.commitDue) * 1000 : 86400000; // default 1d
        const commit = createCommitment({
          reason: options.commitReason,
          suggestedText: options.commitReason,
          dueEarliest: Date.now() + dueMs,
          dueLatest: Date.now() + dueMs + 3600000, // +1h window
          kind: options.commitKind || "open_loop",
          sensitivity: options.commitSensitivity || "routine",
          channel: options.channel || "",
          target: options.target || "",
          agent: options.agent || ""
        });
        process.stdout.write(`Committed: ${formatCommitmentBrief(commit)}\n`);
        return 0;
      }
      case "commitments": {
        expireStaleCommitments();
        const store = loadCommitments();
        const pending = store.commitments.filter(c => c.status === "pending");
        const due = listDueCommitments();
        if (!pending.length) {
          process.stdout.write("No pending commitments.\n");
        } else {
          process.stdout.write("=== Commitments (" + pending.length + " pending, " + due.length + " due) ===\n");
          for (const c of pending) {
            const isDue = due.some(d => d.id === c.id);
            process.stdout.write("  " + (isDue ? "[DUE]" : "[...]") + " " + formatCommitmentBrief(c) + "\n");
          }
        }
        return 0;
      }
      case "commit-done": {
        if (!options.commitId) throw new Error("--commit-done requires an ID");
        const done = completeCommitment(options.commitId);
        process.stdout.write(`Done: ${done.reason}\n`);
        return 0;
      }
      case "commit-cancel": {
        if (!options.commitId) throw new Error("--commit-cancel requires an ID");
        const cancelled = cancelCommitment(options.commitId);
        process.stdout.write(`Cancelled: ${cancelled.reason}\n`);
        return 0;
      }
      case "reply":
        return await handleReply(options);
      case "deliver":
        return await handleDeliver(options.id);
      case "history": {
        const lines = tailHistory(options.historyLimit || 50);
        for (const line of lines) process.stdout.write(`${line}\n`);
        return 0;
      }
      case "stats": {
        process.stdout.write(`${formatStats(queryReminders())}\n`);
        return 0;
      }
      default:
        break;
    }

    if (!options.remindText && !options.taskPrompt) throw new Error("Need --remind or --task");
    if (!options.channel) throw new Error("--channel is required");
    if (!options.target) throw new Error("--target is required");
    if (options.taskPrompt && !options.agent) throw new Error("--agent is required for --task");
    if (options.followupTask && !options.agent) throw new Error("--agent is required for --if-unconfirmed-task");

    const followupKinds = [options.followupRemind, options.followupTask, options.followupCommand].filter(Boolean);
    if (followupKinds.length > 1) {
      throw new Error("Pick one follow-up type: --if-unconfirmed-remind, --if-unconfirmed-task, or --if-unconfirmed-command");
    }
    if (followupKinds.length && !options.followupAfter && !options.followupAfterPokes) {
      throw new Error("Follow-up needs --if-unconfirmed-after or --if-unconfirmed-after-pokes");
    }
    if (options.followupAfter && options.followupAfterPokes) {
      throw new Error("Pick one follow-up trigger: --if-unconfirmed-after or --if-unconfirmed-after-pokes");
    }
    // --if-unconfirmed-after now works with both --once and --on-calendar (heartbeat mode)

    const state = buildCreateState(options);

    if (options.dryRun) {
      // Build a sketch without writing anything or touching the scheduler.
      const sched =
        state.schedule_type === "calendar"
          ? state.on_calendar
          : state.schedule_input || state.next_base_due_at;
      process.stdout.write(
        `DRY-RUN would-create type=${state.kind} schedule=${sched} channel=${state.channel} target=${state.target} agent=${state.agent || "(default)"} pre_stage=${stageSummary(state.pre_stage)} post_stage=${stageSummary(state.post_stage)} next_base_due_at=${state.next_base_due_at || "-"}\n`
      );
      return 0;
    }

    saveReminder(state);
    reschedule(state);
    saveReminder(state);
    appendHistory({
      event: "created",
      id: state.id,
      kind: state.kind,
      channel: state.channel,
      target: state.target,
      schedule_type: state.schedule_type,
      schedule_input: state.schedule_input || state.on_calendar
    });

    const scheduleLabel =
      state.schedule_type === "calendar" ? state.on_calendar : state.schedule_input || state.next_base_due_at || "once";
    const persistLabel = state.catchup === "none" ? "no" : "yes";
    const toneLabel = state.tone || "none";
    const escalationLabel = state.tones_list ? `active (${state.escalation_intervals || "no intervals"})` : "none";
    let followupLabel = "none";
    if (state.followup_task) followupLabel = state.followup_after_seconds ? `task@${options.followupAfter}` : `task@${state.followup_after_pokes}-pokes`;
    if (state.followup_command) followupLabel = state.followup_after_seconds ? `command@${options.followupAfter}` : `command@${state.followup_after_pokes}-pokes`;
    if (state.followup_remind) followupLabel = state.followup_after_seconds ? `remind@${options.followupAfter}` : `remind@${state.followup_after_pokes}-pokes`;
    const pongLabel = state.pong_stage ? state.pong_stage.type : "none";
    process.stdout.write(
      `CREATED id=${state.id} type=${state.kind} schedule=${scheduleLabel} max_pokes=${state.max_pokes} persistent=${persistLabel} catchup=${state.catchup} tone=${toneLabel} escalation=${escalationLabel} pong=${pongLabel} followup=${followupLabel} timer=active\n`
    );
    return 0;
  } catch (error) {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    return 1;
  }
}

export {
  ROOT_DIR,
  RUNTIME_DIR,
  STATE_DIR,
  applyDeliveryMutation,
  buildCreateState,
  classifyReplyHeuristic,
  clearCycleState,
  detailLines,
  earliestWakeAt,
  nextDueBaseOccurrences,
  nextDuePokeOccurrences,
  parseArgs,
  parseDuration,
  queryReminders,
  resolveToneMetadata
};
