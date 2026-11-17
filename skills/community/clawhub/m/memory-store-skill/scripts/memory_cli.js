#!/usr/bin/env node
/**
 * Memory Store CLI Utility — Node.js edition
 *
 * Pure Node built-ins (fs/path/os/crypto/process), zero dependencies.
 * Feature-parity with the Python edition: two-layer store (global/workspace),
 * three-tier visibility (private/shared/global), atomic writes, decay archive,
 * Chinese n-gram retrieval. JSON files are the single source of truth.
 *
 * Usage: memory-store <command> [--key value ...]
 *        node scripts/memory_cli.js <command> [--key value ...]
 */
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const crypto = require("crypto");

// ==============================================================================
// Constants & defaults
// ==============================================================================

const VALID_TYPES = ["workflow", "decision", "fact", "preference", "debug_solution", "state", "event", "relation"];
const VISIBILITIES = ["private", "shared", "global"];
const PRIORITIES = ["P1", "P2", "P3"];
const SCHEMA_VERSION = 2;
const DEFAULT_VISIBILITY = { global: "global", project: "shared", workspace: "shared" };
// Weekly retention factor: larger values decay more slowly.
const PRIORITY_DECAY = { P1: 0.8, P2: 0.5, P3: 0.3 };
const PROJECT_STORE_RELATIVE = path.join(".agents", "memory-store");
const CONFIG_SCHEMA_VERSION = 1;
const DEFAULT_MEMORY_PROFILE = "explicit";
const MEMORY_PROFILES = {
  off: {
    auto_recall: "off",
    auto_store: "off",
    allowed_automatic_types: [],
    max_automatic_memories_per_conversation: 0,
  },
  explicit: {
    auto_recall: "explicit",
    auto_store: "explicit",
    allowed_automatic_types: [],
    max_automatic_memories_per_conversation: 0,
  },
  balanced: {
    auto_recall: "relevant",
    auto_store: "selective",
    allowed_automatic_types: ["decision", "debug_solution", "workflow", "preference"],
    max_automatic_memories_per_conversation: 3,
  },
  proactive: {
    auto_recall: "relevant",
    auto_store: "proactive",
    allowed_automatic_types: VALID_TYPES,
    max_automatic_memories_per_conversation: 5,
  },
};

// Authoritative fallback version. MUST match package.json "version".
// Used when package.json is not present (e.g. deployed skill dir without it).
const VERSION = "1.1.1";

// Legacy platform-specific global stores (pre-v2.8). Used only by `migrate`
// to discover and consolidate memories into the universal store.
const LEGACY_GLOBAL_STORES = {
  claude: path.join(os.homedir(), ".claude", "memory-store"),
  gemini: path.join(os.homedir(), ".gemini", "memory-store"),
  antigravity: path.join(os.homedir(), ".gemini", "config", "memory-store"),
  codex: path.join(os.homedir(), ".agents", "memory-store"),
  opencode: path.join(os.homedir(), ".config", "opencode", "memory-store"),
};

/** Universal global store path — shared across all agent platforms. */
const UNIVERSAL_GLOBAL_STORE = path.join(os.homedir(), ".memory-store");

/** Type icons for SUMMARY.md display. */
const TYPE_ICON = {
  decision: "📐", debug_solution: "🔧", workflow: "🔄",
  preference: "⭐", fact: "📌", state: "📊", event: "📅", relation: "🔗",
};

// ==============================================================================
// Helpers
// ==============================================================================

function nowISO() {
  return new Date().toISOString();
}

function generateId() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  const dateStr = `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
  const rand = crypto.randomBytes(3).toString("hex").slice(0, 6);
  return `mem_${dateStr}_${rand}`;
}

function normalizeScope(scope) {
  return scope === "project" ? "workspace" : scope;
}

function fail(message) {
  process.stderr.write(`Error: ${message}\n`);
  process.exit(1);
}

function requireNonEmpty(value, name) {
  if (typeof value !== "string" || !value.trim()) fail(`--${name} is required and must not be empty.`);
  return value.trim();
}

function validateScope(scope, { allowAll = false } = {}) {
  const normalized = normalizeScope(scope || "global");
  const allowed = allowAll ? ["all", "global", "workspace"] : ["global", "workspace"];
  if (!allowed.includes(normalized)) {
    fail(`Invalid scope '${scope}'. Must be one of: ${allowed.join(", ")}.`);
  }
  return normalized;
}

function validateEnum(value, values, name) {
  if (value !== undefined && !values.includes(value)) {
    fail(`Invalid ${name} '${value}'. Must be one of: ${values.join(", ")}.`);
  }
  return value;
}

function validateNumberInRange(value, name, min = 0, max = 1) {
  const n = Number(value);
  if (!Number.isFinite(n) || n < min || n > max) {
    fail(`--${name} must be a number between ${min} and ${max}.`);
  }
  return n;
}

function validatePositiveInteger(value, name) {
  const raw = typeof value === "string" ? value.trim() : value;
  const n = Number(raw);
  if (!Number.isInteger(n) || n <= 0) fail(`--${name} must be a positive integer.`);
  return n;
}

function validateVisibilityFilter(value) {
  if (!value) return new Set();
  const values = value.split(",").map((v) => v.trim().toLowerCase()).filter(Boolean);
  const invalid = values.filter((v) => !VISIBILITIES.includes(v));
  if (invalid.length) fail(`Invalid visibility value(s): ${invalid.join(", ")}. Must be one of: ${VISIBILITIES.join(", ")}.`);
  return new Set(values);
}

function agentIdentity(a) {
  return a.as_agent || process.env.MEMORY_AGENT_ID || null;
}

function canAccessMemory(mem, asAgent) {
  return mem.visibility !== "private" || Boolean(asAgent && mem.owner_agent === asAgent);
}

function inferPriority(imp) {
  return imp >= 0.8 ? "P1" : imp >= 0.5 ? "P2" : "P3";
}

/** Normalized signature for dedup: type + title + leading summary. */
function memSignature(m) {
  const norm = (s) => (s || "").toString().trim().toLowerCase().replace(/\s+/g, " ");
  return `${m.type || "fact"}|${norm(m.title)}|${norm(m.summary).slice(0, 80)}`;
}

/** Parse --type (comma-separated, multi-value) into a validated Set, or null if absent. */
function parseTypeFilter(typeArg) {
  if (!typeArg) return null;
  const types = typeArg.split(",").map((t) => t.trim().toLowerCase()).filter(Boolean);
  if (!types.length) return null;
  const invalid = types.filter((t) => !VALID_TYPES.includes(t));
  if (invalid.length) {
    process.stderr.write(
      `Error: Invalid memory type(s): ${invalid.join(", ")}. Must be one of: ${VALID_TYPES.join(", ")}\n`
    );
    process.exit(1);
  }
  return new Set(types);
}

/** Read-time normalization: fill v2 fields with defaults (back-compat). */
function defaults(mem, storeScope) {
  const scope = normalizeScope(storeScope || "global");
  const imp = parseFloat(mem.importance ?? 0.5);
  const defs = {
    schema_version: SCHEMA_VERSION,
    scope: scope,
    visibility: DEFAULT_VISIBILITY[scope] || "shared",
    priority: inferPriority(imp),
    status: "active",
    decay_score: imp,
    owner_agent: null,
    write_intent: "explicit",
    embedding: null,
    embedding_model: null,
  };
  for (const [k, v] of Object.entries(defs)) {
    if (mem[k] === undefined || mem[k] === null) mem[k] = v;
  }
  return mem;
}

function detectDefaultStorePath(scope) {
  if (scope === "project" || scope === "workspace") {
    return path.resolve(process.cwd(), PROJECT_STORE_RELATIVE);
  }
  // Universal global store: shared across all agent platforms
  // Always use this path — it's the single source of truth for global memories.
  // Platform-specific paths are only consulted as fallback during migration.
  return path.resolve(UNIVERSAL_GLOBAL_STORE);
}

function resolveStorePath(overridePath, scope) {
  if (overridePath) return path.resolve(overridePath);
  return detectDefaultStorePath(scope);
}

function memoryProfile(profile, source, configPath = null) {
  const settings = MEMORY_PROFILES[profile];
  if (!settings) fail(`Invalid profile '${profile}'. Must be one of: ${Object.keys(MEMORY_PROFILES).join(", ")}.`);
  return {
    schema_version: CONFIG_SCHEMA_VERSION,
    profile,
    ...settings,
    notify_on_automatic_store: true,
    source,
    config_path: configPath,
  };
}

function readMemoryConfig(scope, overridePath) {
  const configPath = path.join(resolveStorePath(overridePath, scope), "config.json");
  if (!fs.existsSync(configPath)) return null;
  try {
    const parsed = JSON.parse(fs.readFileSync(configPath, "utf8"));
    const profile = parsed && parsed.profile;
    if (!MEMORY_PROFILES[profile]) throw new Error(`invalid profile '${profile || "missing"}'`);
    return memoryProfile(profile, scope, configPath);
  } catch (e) {
    fail(`Cannot read memory policy '${configPath}': ${e.message}. The file was not modified.`);
  }
}

function effectiveMemoryConfig(scope = "workspace", overridePath = null) {
  if (overridePath) {
    return readMemoryConfig(scope, overridePath) || memoryProfile(DEFAULT_MEMORY_PROFILE, "default");
  }
  if (scope === "workspace") {
    const workspace = readMemoryConfig("workspace", null);
    if (workspace) return workspace;
  }
  return readMemoryConfig("global", null) || memoryProfile(DEFAULT_MEMORY_PROFILE, "default");
}

function writeMemoryConfig(scope, overridePath, profile) {
  const storePath = resolveStorePath(overridePath, scope);
  const configPath = path.join(storePath, "config.json");
  fs.mkdirSync(storePath, { recursive: true });
  const config = {
    schema_version: CONFIG_SCHEMA_VERSION,
    profile,
    configured_at: nowISO(),
  };
  atomicWriteJson(configPath, config);
  return memoryProfile(profile, scope, configPath);
}

/** Multi-layer path resolution; scope=all + storePath treats it as ROOT (with v1 fallback). */
function resolveTargetPaths(storePathArg, scope) {
  const paths = [];
  const useRoot = Boolean(storePathArg) && scope === "all";
  if (scope === "all" || scope === "global") {
    if (useRoot) {
      const root = path.resolve(storePathArg);
      paths.push(["global", path.join(root, "global")]);
      if (fs.existsSync(path.join(root, "memories.json"))) paths.push(["global", root]);
    } else {
      paths.push(["global", resolveStorePath(storePathArg, "global")]);
    }
  }
  if (scope === "all" || scope === "project" || scope === "workspace") {
    if (useRoot) {
      const root = path.resolve(storePathArg);
      paths.push(["workspace", path.join(root, "workspace")]);
      if (fs.existsSync(path.join(root, "memories.json"))) paths.push(["workspace", root]);
    } else {
      paths.push(["workspace", resolveStorePath(storePathArg, "project")]);
    }
  }
  return paths;
}

function ensureStoreDir(storePath) {
  fs.mkdirSync(storePath, { recursive: true });
  fs.mkdirSync(path.join(storePath, "archive"), { recursive: true });
  const memFile = path.join(storePath, "memories.json");
  if (!fs.existsSync(memFile)) fs.writeFileSync(memFile, "[]\n", "utf8");
  const idxFile = path.join(storePath, "memories.index.json");
  if (!fs.existsSync(idxFile)) fs.writeFileSync(idxFile, "{}\n", "utf8");
}

function loadMemories(storePath) {
  const memFile = path.join(storePath, "memories.json");
  if (!fs.existsSync(memFile)) return [];
  try {
    const parsed = JSON.parse(fs.readFileSync(memFile, "utf8"));
    if (!Array.isArray(parsed)) throw new Error("top-level value must be a JSON array");
    return parsed;
  } catch (e) {
    fail(`Cannot read memory store '${memFile}': ${e.message}. The file was not modified.`);
  }
}

function loadArchiveFiles(storePath, storeScope) {
  const archiveDir = path.join(storePath, "archive");
  if (!fs.existsSync(archiveDir)) return [];
  const records = [];
  for (const name of fs.readdirSync(archiveDir).filter((f) => f.startsWith("archived_") && f.endsWith(".json")).sort()) {
    const file = path.join(archiveDir, name);
    let memories;
    try {
      memories = JSON.parse(fs.readFileSync(file, "utf8"));
      if (!Array.isArray(memories)) throw new Error("top-level value must be a JSON array");
    } catch (e) {
      fail(`Cannot read archive '${file}': ${e.message}. The file was not modified.`);
    }
    for (let i = 0; i < memories.length; i++) {
      const memory = defaults(memories[i], storeScope);
      memory.status = "archived";
      records.push({ memory, file, index: i, memories });
    }
  }
  return records;
}

/** Crash-safe atomic replacement. This is not a multi-process transaction. */
function atomicWriteJson(file, data) {
  const tmp = `${file}.${process.pid}.${crypto.randomBytes(4).toString("hex")}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + "\n", "utf8");
  fs.renameSync(tmp, file);
}

function saveMemories(storePath, memories) {
  ensureStoreDir(storePath);
  const memFile = path.join(storePath, "memories.json");
  atomicWriteJson(memFile, memories);
  rebuildIndex(storePath, memories);
  updateSummary(storePath, memories);
}

/** Compute a composite score for summary ranking: importance × recency boost. */
function summaryScore(mem) {
  const imp = parseFloat(mem.importance || 0.5);
  let recency = 1.0;
  if (mem.created_at) {
    const days = (Date.now() - new Date(mem.created_at).getTime()) / 86400000;
    recency = Math.exp(-0.02 * days); // gentle decay over ~50 days
  }
  return imp * recency;
}

/** Maintain SUMMARY.md — a human/agent-readable snapshot of top memories. */
function updateSummary(storePath, memories) {
  if (!memories || memories.length === 0) {
    fs.writeFileSync(path.join(storePath, "SUMMARY.md"),
      "# Memory Store Summary\n\n_No memories yet._\n", "utf8");
    return;
  }

  // Rank: composite score descending, take top 10
  const ranked = memories
    .filter((m) => m.status !== "archived")
    .map((m) => ({ mem: m, score: summaryScore(m) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

  const lines = [];
  lines.push("# Memory Store Summary\n");
  lines.push(`_Last updated: ${nowISO()}_\n`);
  lines.push(`Total memories: ${memories.length} | Showing top ${ranked.length}\n`);
  lines.push("---\n");

  for (const { mem, score } of ranked) {
    const icon = TYPE_ICON[mem.type] || "📄";
    const p = mem.priority || "P2";
    const imp = mem.importance || "—";
    const scope = mem.scope === "workspace" ? "📁" : "🌐";
    lines.push(`### ${icon} ${mem.type}: ${mem.title}`);
    lines.push(`**Priority:** ${p} · **Importance:** ${imp} · **Scope:** ${scope} ${mem.scope || "global"}`);
    if (mem.summary) lines.push(mem.summary);
    if (mem.tags && mem.tags.length) lines.push(`\`tags: ${mem.tags.join(", ")}\``);
    lines.push("");
  }

  lines.push("---\n");
  lines.push("_Run `memory-store search --query \"...\"` for full-text search._\n");

  fs.writeFileSync(path.join(storePath, "SUMMARY.md"), lines.join("\n"), "utf8");
}

function rebuildIndex(storePath, memories) {
  const index = {};
  for (const mem of memories) {
    const text = `${mem.title || ""} ${mem.summary || ""} ${mem.details || ""} ${(mem.tags || []).join(" ")}`.toLowerCase();
    const tokens = new Set(text.match(/[\w\u4e00-\u9fff]+/g) || []);
    for (const t of tokens) {
      if (t.length >= 2) {
        if (!index[t]) index[t] = [];
        index[t].push(mem.id);
      }
    }
  }
  fs.writeFileSync(path.join(storePath, "memories.index.json"), JSON.stringify(index, null, 2) + "\n", "utf8");
}

function writeOutput(data, outputFile) {
  const json = JSON.stringify(data, null, 2) + "\n";
  if (!outputFile) {
    process.stdout.write(json);
    return;
  }
  const out = path.resolve(outputFile);
  try {
    const st = fs.existsSync(out) ? fs.statSync(out) : null;
    if (st && st.isDirectory()) {
      process.stderr.write(`Error: --output path is a directory, not a file: ${out}\n`);
      process.exit(1);
    }
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, json, "utf8");
  } catch (e) {
    process.stderr.write(`Error: Cannot write output to '${out}': ${e.message}\n`);
    process.exit(1);
  }
  process.stdout.write(`Success! Output written to: ${out}\n`);
}

// ==============================================================================
// Search & scoring (incl. Chinese n-gram windows)
// ==============================================================================

const CN_RUN = /[\u4e00-\u9fff]+/;

/** Splits a query into [origToken, [cnNGrams]] units for substring scoring. */
function expandQueryUnits(query) {
  const units = [];
  for (const tok of query.split(/\s+/)) {
    if (!tok) continue;
    const cnRuns = tok.match(CN_RUN) || [];
    if (cnRuns.length) {
      const grams = [];
      for (const run of cnRuns) {
        if (run.length >= 3) {
          for (const n of [4, 3, 2]) {
            for (let i = 0; i <= run.length - n; i++) grams.push(run.slice(i, i + n));
          }
        } else {
          grams.push(run);
        }
      }
      units.push([tok, grams]);
    } else {
      units.push([tok, []]);
    }
  }
  return units;
}

function calcScore(mem, rawQuery, filterTags, filterTypes) {
  if (filterTypes && !filterTypes.has(mem.type)) return 0;
  const memTags = new Set((mem.tags || []).map((t) => t.toLowerCase()));
  if (filterTags.size && ![...filterTags].every((t) => memTags.has(t))) return 0;

  const text = `${mem.title || ""} ${mem.summary || ""} ${mem.details || ""}`.toLowerCase();

  let keyword = 0;
  if (rawQuery) {
    const units = expandQueryUnits(rawQuery.toLowerCase());
    let matches = 0;
    for (const [orig, grams] of units) {
      if (text.includes(orig) || grams.some((g) => text.includes(g))) matches++;
    }
    keyword = units.length ? matches / units.length : 0;
  } else {
    keyword = 1;
  }
  if (rawQuery && keyword === 0 && !filterTags.size) return 0;

  let tagScore = 0;
  if (rawQuery && memTags.size) {
    const units = expandQueryUnits(rawQuery.toLowerCase());
    let m = 0;
    for (const [orig, grams] of units) {
      let hit = false;
      for (const tag of memTags) {
        if (orig.includes(tag) || tag.includes(orig) || grams.some((g) => tag.includes(g))) {
          hit = true;
          break;
        }
      }
      if (hit) m++;
    }
    tagScore = units.length ? m / units.length : 0;
  } else {
    tagScore = memTags.size ? 0.5 : 0;
  }

  const typeScore = filterTypes ? 1.0 : 0.5;

  let recency = 0.5;
  if (mem.created_at) {
    const days = Math.max(0, (Date.now() - new Date(mem.created_at).getTime()) / 86400000);
    recency = Math.exp(-0.01 * days);
  }

  const importance = parseFloat(mem.importance ?? 0.5);
  const total = 0.4 * keyword + 0.25 * tagScore + 0.2 * typeScore + 0.1 * recency + 0.05 * importance;
  return +total.toFixed(4);
}

/** Ebbinghaus-style decay: accessed memories decay slower, P1 slowest. */
function computeDecay(mem) {
  const imp = parseFloat(mem.importance ?? 0.5);
  const pDecay = PRIORITY_DECAY[mem.priority || inferPriority(imp)] || 0.5;
  const acc = parseInt(mem.access_count ?? 0, 10) || 0;
  let days = 0;
  const last = mem.last_accessed || mem.created_at;
  if (last) {
    const lastTime = new Date(last).getTime();
    days = Number.isFinite(lastTime) ? Math.max(0, (Date.now() - lastTime) / 86400000) : 0;
  }
  const stability = 1 + 0.2 * Math.log10(acc + 1);
  const score = imp * Math.pow(pDecay, days / 7) * stability;
  return +Math.min(1, Math.max(0, score)).toFixed(4);
}

// ==============================================================================
// Subcommand handlers
// ==============================================================================

function cmdInit(a) {
  const scope = validateScope(a.scope || "global");
  const storePath = resolveStorePath(a.store_path, scope);
  ensureStoreDir(storePath);
  process.stdout.write(`Initialized memory store at: ${storePath}\n`);
}

function cmdConfig(a) {
  const action = (a.action || "show").toLowerCase();
  const requestedScope = (a.scope || (action === "show" ? "effective" : "global")).toLowerCase();
  if (!["global", "workspace", "effective"].includes(requestedScope)) {
    fail("--scope must be one of: global, workspace, effective.");
  }
  if (action === "show") {
    const config = requestedScope === "effective"
      ? effectiveMemoryConfig("workspace", a.store_path)
      : readMemoryConfig(requestedScope, a.store_path) || memoryProfile(DEFAULT_MEMORY_PROFILE, "default");
    writeOutput(config, a.output);
    return;
  }
  if (requestedScope === "effective") fail("config set/reset requires --scope global or workspace.");
  if (action === "set") {
    const profile = requireNonEmpty(a.profile, "profile").toLowerCase();
    if (!MEMORY_PROFILES[profile]) {
      fail(`Invalid profile '${profile}'. Must be one of: ${Object.keys(MEMORY_PROFILES).join(", ")}.`);
    }
    writeOutput(writeMemoryConfig(requestedScope, a.store_path, profile), a.output);
    return;
  }
  if (action === "reset") {
    const configPath = path.join(resolveStorePath(a.store_path, requestedScope), "config.json");
    if (fs.existsSync(configPath)) fs.unlinkSync(configPath);
    writeOutput({ reset: true, scope: requestedScope, config_path: configPath }, a.output);
    return;
  }
  fail("config action must be one of: show, set, reset.");
}

function cmdStore(a) {
  if (!VALID_TYPES.includes(a.type)) {
    process.stderr.write(`Error: Invalid memory type '${a.type}'. Must be one of: ${VALID_TYPES.join(", ")}\n`);
    process.exit(1);
  }
  const title = requireNonEmpty(a.title, "title");
  const summary = requireNonEmpty(a.summary, "summary");
  const scopeName = validateScope(a.scope || "global");
  const intent = (a.intent || "explicit").toLowerCase();
  validateEnum(intent, ["explicit", "automatic"], "intent");
  const policy = effectiveMemoryConfig(scopeName, a.store_path);
  if (intent === "automatic") {
    if (policy.auto_store === "off" || policy.auto_store === "explicit") {
      fail(`Automatic storage is disabled by the '${policy.profile}' memory profile.`);
    }
    if (!policy.allowed_automatic_types.includes(a.type)) {
      fail(`Memory type '${a.type}' is not allowed for automatic storage by the '${policy.profile}' profile.`);
    }
    requireNonEmpty(a.source_conv_id, "source-conv-id");
  }
  const visibility = a.visibility || DEFAULT_VISIBILITY[scopeName] || "shared";
  validateEnum(visibility, VISIBILITIES, "visibility");
  if (a.priority !== undefined) validateEnum(a.priority, PRIORITIES, "priority");
  const importance = validateNumberInRange(a.importance ?? 0.5, "importance");
  const ttlDays = a.ttl_days !== undefined ? validatePositiveInteger(a.ttl_days, "ttl-days") : null;
  const ownerAgent = a.agent_id || process.env.MEMORY_AGENT_ID || null;
  if (visibility === "private" && !ownerAgent) {
    fail("--agent-id or MEMORY_AGENT_ID is required when storing a private memory.");
  }
  const storePath = resolveStorePath(a.store_path, scopeName);
  const memories = loadMemories(storePath);
  if (intent === "automatic") {
    const automaticCount = memories.filter(
      (m) => m.source_conversation_id === a.source_conv_id && (m.write_intent || "explicit") === "automatic"
    ).length;
    if (automaticCount >= policy.max_automatic_memories_per_conversation) {
      fail(
        `Automatic memory limit reached for conversation '${a.source_conv_id}' ` +
        `(${policy.max_automatic_memories_per_conversation}, profile=${policy.profile}).`
      );
    }
  }
  const tags = a.tags ? a.tags.split(",").map((t) => t.trim().toLowerCase()) : [];
  const relatedFiles = a.related_files ? a.related_files.split(",").map((f) => f.trim()) : [];
  const expiresAt = ttlDays === null ? null : new Date(Date.now() + ttlDays * 86400000).toISOString();
  const mem = {
    id: generateId(),
    schema_version: SCHEMA_VERSION,
    scope: scopeName,
    visibility: visibility,
    owner_agent: ownerAgent,
    created_at: nowISO(),
    updated_at: nowISO(),
    source_conversation_id: a.source_conv_id || null,
    write_intent: intent,
    type: a.type,
    title,
    summary,
    details: a.details || null,
    tags: tags,
    importance: importance,
    priority: a.priority || inferPriority(importance),
    access_count: 0,
    last_accessed: null,
    related_files: relatedFiles,
    ttl_days: ttlDays,
    expires_at: expiresAt,
    decay_score: importance,
    status: "active",
    embedding: null,
    embedding_model: null,
  };
  memories.push(mem);
  saveMemories(storePath, memories);
  process.stdout.write(
    `Stored memory [${mem.id}] successfully in ${storePath} (scope=${mem.scope}, visibility=${mem.visibility})\n`
  );
}

function searchMemories(a) {
  const scope = validateScope(a.scope || "all", { allowAll: true });
  const intent = (a.intent || "explicit").toLowerCase();
  validateEnum(intent, ["explicit", "automatic"], "intent");
  if (intent === "automatic") {
    const policy = effectiveMemoryConfig(scope === "global" ? "global" : "workspace", a.store_path);
    if (policy.auto_recall === "off" || policy.auto_recall === "explicit") {
      fail(`Automatic recall is disabled by the '${policy.profile}' memory profile.`);
    }
  }
  const limit = validatePositiveInteger(a.limit ?? 5, "limit");
  const query = a.query || "";
  const filterTags = new Set(a.tags ? a.tags.split(",").map((t) => t.trim().toLowerCase()) : []);
  const filterTypes = parseTypeFilter(a.type);
  const visibilityFilter = validateVisibilityFilter(a.visibility);
  const asAgent = agentIdentity(a);

  const targetPaths = resolveTargetPaths(a.store_path, scope);
  const results = [];
  const seen = new Set();

  for (const [scopeName, p] of targetPaths) {
    for (let m of loadMemories(p)) {
      if (seen.has(m.id)) continue;
      m = defaults(m, scopeName);
      if (!canAccessMemory(m, asAgent)) continue;
      if (visibilityFilter.size && !visibilityFilter.has(m.visibility)) continue;
      const score = calcScore(m, query, filterTags, filterTypes);
      if (score > 0) {
        seen.add(m.id);
        results.push({ memory: { ...m, _score: score, _store_scope: scopeName }, storePath: p });
      }
    }
  }
  results.sort((x, y) => (y.memory._score - x.memory._score) || (y.memory.created_at || "").localeCompare(x.memory.created_at || ""));
  const selected = results.slice(0, limit);
  if (a.touch) {
    const byStore = new Map();
    for (const result of selected) {
      if (!byStore.has(result.storePath)) byStore.set(result.storePath, []);
      byStore.get(result.storePath).push(result);
    }
    for (const [storePath, storeResults] of byStore) {
      const mems = loadMemories(storePath);
      for (const result of storeResults) {
        const idx = mems.findIndex((m) => m.id === result.memory.id);
        if (idx < 0) continue;
        mems[idx].access_count = (mems[idx].access_count || 0) + 1;
        mems[idx].last_accessed = nowISO();
        result.memory.access_count = mems[idx].access_count;
        result.memory.last_accessed = mems[idx].last_accessed;
      }
      saveMemories(storePath, mems);
    }
  }
  return selected.map((r) => r.memory);
}

function cmdSearch(a) {
  writeOutput(searchMemories(a), a.output);
}

function cmdRecall(a) {
  requireNonEmpty(a.id, "id");
  const scope = a.scope ? validateScope(a.scope, { allowAll: true }) : (a.store_path ? "global" : "all");
  const targets = resolveTargetPaths(a.store_path, scope);
  const asAgent = agentIdentity(a);
  for (const [scopeName, p] of targets) {
    const mems = loadMemories(p);
    const idx = mems.findIndex((m) => m.id === a.id);
    if (idx >= 0) {
      const m = defaults(mems[idx], scopeName);
      if (!canAccessMemory(m, asAgent)) fail(`Memory with ID '${a.id}' was not found or access was denied.`);
      m.access_count = (m.access_count || 0) + 1;
      m.last_accessed = nowISO();
      mems[idx] = m;
      saveMemories(p, mems);
      writeOutput(m, a.output);
      return;
    }
    const archived = loadArchiveFiles(p, scopeName);
    const record = archived.find((r) => r.memory.id === a.id);
    if (record) {
      if (!canAccessMemory(record.memory, asAgent)) fail(`Memory with ID '${a.id}' was not found or access was denied.`);
      record.memory.access_count = (record.memory.access_count || 0) + 1;
      record.memory.last_accessed = nowISO();
      record.memories[record.index] = record.memory;
      atomicWriteJson(record.file, record.memories);
      writeOutput(record.memory, a.output);
      return;
    }
  }
  process.stderr.write(`Error: Memory with ID '${a.id}' not found.\n`);
  process.exit(1);
}

function cmdList(a) {
  const scope = validateScope(a.scope || "global", { allowAll: true });
  const limit = validatePositiveInteger(a.limit ?? 20, "limit");
  if (a.status !== undefined && !["active", "archived"].includes(a.status)) fail("--status must be active or archived.");
  const targetPaths = resolveTargetPaths(a.store_path, scope);
  const asAgent = agentIdentity(a);
  let mems = [];
  for (const [scopeName, p] of targetPaths) {
    if (a.status !== "archived") {
      for (let m of loadMemories(p)) {
        m = defaults(m, scopeName);
        m._store_scope = scopeName;
        mems.push(m);
      }
    }
    if (a.status === "archived" || a.include_archived) {
      for (const record of loadArchiveFiles(p, scopeName)) {
        mems.push({ ...record.memory, _store_scope: scopeName });
      }
    }
  }
  mems = mems.filter((m) => canAccessMemory(m, asAgent));
  if (a.type) {
    const filterTypes = parseTypeFilter(a.type);
    if (filterTypes) mems = mems.filter((m) => filterTypes.has(m.type));
  }
  if (a.tags) {
    const req = new Set(a.tags.split(",").map((t) => t.trim().toLowerCase()));
    mems = mems.filter((m) => req.size && [...req].every((t) => (m.tags || []).includes(t)));
  }
  if (a.status) mems = mems.filter((m) => m.status === a.status);
  if (a.visibility) {
    const vs = validateVisibilityFilter(a.visibility);
    mems = mems.filter((m) => vs.has(m.visibility));
  }
  const sortKey = a.sort_by || "created_at";
  if (sortKey === "importance") mems.sort((x, y) => parseFloat(y.importance || 0) - parseFloat(x.importance || 0));
  else if (sortKey === "access_count") mems.sort((x, y) => (y.access_count || 0) - (x.access_count || 0));
  else mems.sort((x, y) => (y.created_at || "").localeCompare(x.created_at || ""));
  writeOutput(mems.slice(0, limit), a.output);
}

function cmdUpdate(a) {
  requireNonEmpty(a.id, "id");
  const scope = a.scope ? validateScope(a.scope, { allowAll: true }) : (a.store_path ? "global" : "all");
  const asAgent = agentIdentity(a);
  for (const [scopeName, storePath] of resolveTargetPaths(a.store_path, scope)) {
    const mems = loadMemories(storePath);
    const idx = mems.findIndex((m) => m.id === a.id);
    if (idx < 0) continue;
    const m = defaults(mems[idx], scopeName);
    if (!canAccessMemory(m, asAgent)) fail(`Memory ID '${a.id}' was not found or access was denied.`);
    if (a.title !== undefined) m.title = requireNonEmpty(a.title, "title");
    if (a.summary !== undefined) m.summary = requireNonEmpty(a.summary, "summary");
    if (a.details !== undefined) m.details = a.details;
    if (a.tags !== undefined) m.tags = a.tags.split(",").map((t) => t.trim().toLowerCase()).filter(Boolean);
    if (a.importance !== undefined) {
      m.importance = validateNumberInRange(a.importance, "importance");
      m.decay_score = m.importance;
    }
    if (a.visibility !== undefined) {
      validateEnum(a.visibility, VISIBILITIES, "visibility");
      if (a.visibility === "private" && m.visibility !== "private") {
        if (!asAgent) fail("--as-agent or MEMORY_AGENT_ID is required when changing a memory to private.");
        m.owner_agent = asAgent;
      }
      m.visibility = a.visibility;
    }
    if (a.priority !== undefined) {
      validateEnum(a.priority, PRIORITIES, "priority");
      m.priority = a.priority;
    }
    if (a.ttl_days !== undefined) {
      m.ttl_days = validatePositiveInteger(a.ttl_days, "ttl-days");
      m.expires_at = new Date(Date.now() + m.ttl_days * 86400000).toISOString();
    }
    m.updated_at = nowISO();
    mems[idx] = m;
    saveMemories(storePath, mems);
    process.stdout.write(`Updated memory [${a.id}] in ${storePath}\n`);
    return;
  }
  fail(`Memory ID '${a.id}' not found.`);
}

function cmdDelete(a) {
  requireNonEmpty(a.id, "id");
  const scope = a.scope ? validateScope(a.scope, { allowAll: true }) : (a.store_path ? "global" : "all");
  const asAgent = agentIdentity(a);
  for (const [scopeName, p] of resolveTargetPaths(a.store_path, scope)) {
    const mems = loadMemories(p);
    const idx = mems.findIndex((m) => m.id === a.id);
    if (idx >= 0) {
      const m = defaults(mems[idx], scopeName);
      if (!canAccessMemory(m, asAgent)) fail(`Memory ID '${a.id}' was not found or access was denied.`);
      mems.splice(idx, 1);
      saveMemories(p, mems);
      process.stdout.write(`Deleted memory [${a.id}] from ${p}\n`);
      return;
    }
    const record = loadArchiveFiles(p, scopeName).find((r) => r.memory.id === a.id);
    if (record) {
      if (!canAccessMemory(record.memory, asAgent)) fail(`Memory ID '${a.id}' was not found or access was denied.`);
      record.memories.splice(record.index, 1);
      atomicWriteJson(record.file, record.memories);
      process.stdout.write(`Deleted archived memory [${a.id}] from ${record.file}\n`);
      return;
    }
  }
  fail(`Memory ID '${a.id}' not found.`);
}

function cmdMerge(a) {
  requireNonEmpty(a.ids, "ids");
  const scopeName = validateScope(a.scope || "global");
  const ids = [...new Set(a.ids.split(",").map((s) => s.trim()).filter(Boolean))];
  if (ids.length < 2) {
    fail("Specify at least 2 distinct memory IDs to merge.");
  }
  const storePath = resolveStorePath(a.store_path, scopeName);
  const mems = loadMemories(storePath);
  const targets = mems.filter((m) => ids.includes(m.id)).map((m) => defaults(m, scopeName));
  if (targets.length !== ids.length) {
    fail("Could not find all specified memory IDs in the store.");
  }
  const asAgent = agentIdentity(a);
  if (targets.some((m) => !canAccessMemory(m, asAgent))) fail("One or more memories were not found or access was denied.");
  const allTags = [...new Set(targets.flatMap((t) => t.tags || []))].sort();
  const maxImp = Math.max(...targets.map((t) => parseFloat(t.importance || 0)));
  const allFiles = [...new Set(targets.flatMap((t) => t.related_files || []))].sort();
  const visibility = targets.some((m) => m.visibility === "private")
    ? "private"
    : targets.some((m) => m.visibility === "shared") ? "shared" : "global";
  const merged = defaults({
    id: generateId(),
    created_at: nowISO(),
    updated_at: nowISO(),
    source_conversation_id: null,
    type: targets[0].type || "fact",
    title: `Merged: ${targets[0].title || ""}`,
    summary: targets.map((t) => t.summary || "").join(" | "),
    details: `Merged from original IDs: ${ids.join(", ")}`,
    tags: allTags,
    importance: maxImp,
    visibility,
    owner_agent: visibility === "private" ? asAgent : null,
    access_count: targets.reduce((s, t) => s + (t.access_count || 0), 0),
    last_accessed: nowISO(),
    related_files: allFiles,
    ttl_days: null,
  }, scopeName);
  const remaining = mems.filter((m) => !ids.includes(m.id));
  remaining.push(merged);
  saveMemories(storePath, remaining);
  writeOutput(merged, a.output);
}

function cmdArchive(a) {
  const scope = validateScope(a.scope || "global", { allowAll: true });
  const asAgent = agentIdentity(a);
  const minDecay = validateNumberInRange(a.min_decay ?? 0.15, "min-decay");
  const beforeDays = a.before_days !== undefined ? validatePositiveInteger(a.before_days, "before-days") : null;
  const minImportance = a.min_importance !== undefined
    ? validateNumberInRange(a.min_importance, "min-importance") : null;
  const now = new Date();
  const allArchived = [];

  for (const [scopeName, storePath] of resolveTargetPaths(a.store_path, scope)) {
    const mems = loadMemories(storePath);
    const toArchive = [];
    const toKeep = [];
    for (let m of mems) {
      m = defaults(m, scopeName);
      // Bulk maintenance must not mutate another Agent's private records.
      if (!canAccessMemory(m, asAgent)) {
        toKeep.push(m);
        continue;
      }
      let reason = null;
      if (a.apply_decay) m.decay_score = computeDecay(m);
      const createdTime = new Date(m.created_at).getTime();
      const daysOld = Number.isFinite(createdTime) ? Math.max(0, (now.getTime() - createdTime) / 86400000) : 0;
      if (m.ttl_days && daysOld >= m.ttl_days) {
        reason = `TTL expired (${daysOld.toFixed(1)} >= ${m.ttl_days} days)`;
      } else if (beforeDays !== null && daysOld >= beforeDays && (m.access_count || 0) < 2) {
        reason = `Older than ${beforeDays} days and low access count`;
      } else if (minImportance !== null && parseFloat(m.importance || 0) < minImportance) {
        reason = `Importance below threshold (${m.importance} < ${minImportance})`;
      } else if (parseFloat(m.decay_score || 0) < minDecay) {
        reason = `Decay below threshold (${m.decay_score} < ${minDecay})`;
      }
      if (reason) {
        m.status = "archived";
        m.archived_at = now.toISOString();
        m._archive_reason = reason;
        toArchive.push(m);
      } else {
        toKeep.push(m);
      }
    }
    if (toArchive.length) {
      const archiveDir = path.join(storePath, "archive");
      const archiveFile = path.join(archiveDir, `archived_${now.toISOString().slice(0, 7).replace("-", "")}.json`);
      let existing = [];
      if (fs.existsSync(archiveFile)) {
        try {
          existing = JSON.parse(fs.readFileSync(archiveFile, "utf8"));
          if (!Array.isArray(existing)) throw new Error("top-level value must be a JSON array");
        } catch (e) {
          fail(`Cannot read archive '${archiveFile}': ${e.message}. The file was not modified.`);
        }
      }
      fs.mkdirSync(archiveDir, { recursive: true });
      // Write the archive first: a crash can leave duplicates, but cannot lose the only copy.
      atomicWriteJson(archiveFile, existing.concat(toArchive));
      allArchived.push(...toArchive);
      process.stdout.write(`Archived ${toArchive.length} memories to: ${archiveFile}\n`);
    }
    if (toArchive.length || a.apply_decay) saveMemories(storePath, toKeep);
  }
  writeOutput(allArchived, a.output);
}

function cmdRestore(a) {
  requireNonEmpty(a.id, "id");
  const scope = a.scope ? validateScope(a.scope, { allowAll: true }) : (a.store_path ? "global" : "all");
  const asAgent = agentIdentity(a);
  for (const [scopeName, storePath] of resolveTargetPaths(a.store_path, scope)) {
    const record = loadArchiveFiles(storePath, scopeName).find((r) => r.memory.id === a.id);
    if (!record) continue;
    if (!canAccessMemory(record.memory, asAgent)) fail(`Memory ID '${a.id}' was not found or access was denied.`);
    const active = loadMemories(storePath);
    if (active.some((m) => m.id === a.id)) fail(`Cannot restore '${a.id}': an active memory with the same ID already exists.`);
    const restored = { ...record.memory, status: "active", updated_at: nowISO() };
    delete restored.archived_at;
    delete restored._archive_reason;
    active.push(restored);
    // Write active first: a crash can leave duplicates, but cannot lose the only copy.
    saveMemories(storePath, active);
    record.memories.splice(record.index, 1);
    atomicWriteJson(record.file, record.memories);
    writeOutput(restored, a.output);
    return;
  }
  fail(`Archived memory ID '${a.id}' not found.`);
}

function cmdStats(a) {
  const scope = validateScope(a.scope || "global", { allowAll: true });
  const targetPaths = resolveTargetPaths(a.store_path, scope);
  const asAgent = agentIdentity(a);
  const mems = [];
  for (const [scopeName, p] of targetPaths) {
    for (let m of loadMemories(p)) {
      m = defaults(m, scopeName);
      if (canAccessMemory(m, asAgent)) mems.push(m);
    }
  }
  const typeCounts = {};
  const tagCounts = {};
  const scopeCounts = {};
  const visCounts = {};
  const statusCounts = {};
  let totalImp = 0;
  for (const m of mems) {
    typeCounts[m.type || "unknown"] = (typeCounts[m.type || "unknown"] || 0) + 1;
    for (const t of m.tags || []) tagCounts[t] = (tagCounts[t] || 0) + 1;
    scopeCounts[m.scope || "unknown"] = (scopeCounts[m.scope || "unknown"] || 0) + 1;
    visCounts[m.visibility || "unknown"] = (visCounts[m.visibility || "unknown"] || 0) + 1;
    statusCounts[m.status || "active"] = (statusCounts[m.status || "active"] || 0) + 1;
    totalImp += parseFloat(m.importance || 0);
  }
  const topTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  const mostAccessed = mems
    .map((m) => ({ id: m.id, title: m.title, access_count: m.access_count || 0 }))
    .sort((a, b) => b.access_count - a.access_count)
    .slice(0, 5);
  writeOutput(
    {
      store_path: targetPaths.map(([, p]) => p),
      total_memories: mems.length,
      avg_importance: mems.length ? +(totalImp / mems.length).toFixed(3) : 0,
      scope_breakdown: scopeCounts,
      visibility_breakdown: visCounts,
      status_breakdown: statusCounts,
      type_breakdown: typeCounts,
      top_tags: Object.fromEntries(topTags),
      most_accessed: mostAccessed,
    },
    a.output
  );
}

/**
 * Extract a memory-relevant fragment from one transcript step.
 * Supports two formats:
 *   - Antigravity transcript: { type: "USER_INPUT" | "PLANNER_RESPONSE", ... }
 *   - Generic chat log:       { role: "user"|"assistant"|"system", content|text }
 * Returns a fragment object, or null if the step is not recognizable.
 */
function extractFragment(step) {
  if (!step || typeof step !== "object") return null;
  if (step.type === "USER_INPUT") {
    return { role: "user", content: (step.content || "").slice(0, 1000) };
  }
  if (step.type === "PLANNER_RESPONSE") {
    const toolCalls = step.tool_calls || [];
    const toolNames = toolCalls
      .filter((tc) => typeof tc === "object")
      .map((tc) => tc.name || tc.tool_name || "");
    return {
      role: "assistant",
      summary: (step.content || "").slice(0, 500) || "Tool calls executed",
      tools_used: toolNames,
    };
  }
  const role = (step.role || "").toString().toLowerCase();
  if (role === "user" || role === "assistant" || role === "system") {
    const c = step.content || step.text || "";
    return { role, content: c.slice(0, 1000) };
  }
  return null;
}

function cmdCompress(a) {
  const input = path.resolve(a.input);
  if (!fs.existsSync(input)) {
    process.stderr.write(`Error: Transcript file not found at ${input}\n`);
    process.exit(1);
  }
  const fragments = [];
  let detectedFormat = "unknown";

  // Pass 1: per-line JSON (Antigravity JSONL / one-object-per-line chat logs)
  for (const line of fs.readFileSync(input, "utf8").split("\n")) {
    if (!line.trim()) continue;
    let step;
    try {
      step = JSON.parse(line);
    } catch (e) {
      continue;
    }
    const f = extractFragment(step);
    if (f) {
      fragments.push(f);
      detectedFormat = step.type ? "antigravity" : "generic-chat";
    }
  }

  // Pass 2: whole-file JSON array (single-line or pretty-printed)
  if (fragments.length === 0) {
    try {
      const arr = JSON.parse(fs.readFileSync(input, "utf8"));
      if (Array.isArray(arr)) {
        for (const obj of arr) {
          const f = extractFragment(obj);
          if (f) {
            fragments.push(f);
            detectedFormat = obj.type ? "antigravity" : "generic-chat";
          }
        }
      }
    } catch (e) {
      /* not a JSON array */
    }
  }

  if (fragments.length === 0) {
    process.stderr.write(
      "Warning: No recognizable transcript fragments found. Supported formats: Antigravity transcript " +
        "(type USER_INPUT/PLANNER_RESPONSE) and generic chat ({role, content|text}). For other platforms, " +
        "store memories manually with the `store` subcommand.\n"
    );
  }

  writeOutput(
    {
      source_transcript: input,
      detected_format: detectedFormat,
      extracted_steps_count: fragments.length,
      conversation_fragments: fragments,
      instructions_for_agent:
        "Review the extracted conversation fragments above. Identify key decisions, workflows, facts, preferences, or debug solutions. Summarize each into a concise memory entry and call `store` subcommand to persist. For platforms whose transcript format is unsupported, summarize manually and call `store` directly.",
    },
    a.output
  );
}

function cmdMigrate(a) {
  const targetStore = resolveStorePath(a.store_path, "global"); // universal: ~/.memory-store
  const targetMems = loadMemories(targetStore);
  const seenIds = new Set(targetMems.map((m) => m.id));
  const seenSig = new Set(targetMems.map((m) => memSignature(defaults(m, "global"))));

  const dryRun = a.dry_run === true || a["dry-run"] === true;
  const sourcesFound = [];
  let migrated = 0;
  let skipped = 0;

  for (const [platform, legacyPath] of Object.entries(LEGACY_GLOBAL_STORES)) {
    const memFile = path.join(legacyPath, "memories.json");
    if (!fs.existsSync(memFile)) continue;
    const legacyMems = loadMemories(legacyPath);
    if (!legacyMems.length) continue;

    const archived = [];
    const archiveDir = path.join(legacyPath, "archive");
    if (fs.existsSync(archiveDir)) {
      for (const f of fs.readdirSync(archiveDir)) {
        if (!f.startsWith("archived_") || !f.endsWith(".json")) continue;
        try {
          const arr = JSON.parse(fs.readFileSync(path.join(archiveDir, f), "utf8"));
          if (!Array.isArray(arr)) throw new Error("top-level value must be a JSON array");
          archived.push(...arr);
        } catch (e) {
          fail(`Cannot read legacy archive '${path.join(archiveDir, f)}': ${e.message}. Migration was stopped.`);
        }
      }
    }

    sourcesFound.push({
      platform,
      path: legacyPath,
      active: legacyMems.length,
      archived: archived.length,
    });

    const candidates = legacyMems.concat(archived);
    for (let m of candidates) {
      m = defaults(m, "global");
      if (seenIds.has(m.id) || seenSig.has(memSignature(m))) {
        skipped++;
        continue;
      }
      seenSig.add(memSignature(m));
      seenIds.add(m.id);
      targetMems.push(m);
      migrated++;
    }
  }

  if (migrated > 0 && !dryRun) {
    saveMemories(targetStore, targetMems);
  }

  const report = {
    target_store: targetStore,
    dry_run: dryRun,
    sources_found: sourcesFound,
    migrated,
    skipped,
    total_now: targetMems.length,
  };
  if (dryRun) {
    process.stdout.write(
      `[dry-run] Would migrate ${migrated} memories (skip ${skipped}) into ${targetStore}\n`
    );
  }
  writeOutput(report, a.output);
}

function cmdVersion(a) {
  let version = VERSION;
  // Prefer package.json when present (dev context); fall back to the
  // authoritative VERSION constant above (deployed skill without package.json).
  try {
    const pkg = JSON.parse(
      fs.readFileSync(path.join(__dirname, "..", "package.json"), "utf8")
    );
    version = pkg.version || version;
  } catch (e) {
    /* fall back to VERSION constant */
  }
  const info = {
    name: "memory-store",
    version,
    runtime: "node",
    note: "Pure Node.js implementation — zero dependencies, no Python required.",
  };
  if (a.output) {
    writeOutput(info, a.output);
  } else {
    process.stdout.write(`${info.name} v${info.version} (${info.runtime})\n`);
  }
}

// ==============================================================================
// Intent-oriented facade
// ==============================================================================

function packageVersion() {
  try {
    return JSON.parse(fs.readFileSync(path.join(__dirname, "..", "package.json"), "utf8")).version || VERSION;
  } catch (e) {
    return VERSION;
  }
}

function leadingPositionals(argv) {
  const values = [];
  for (const value of argv.slice(1)) {
    if (value.startsWith("--")) break;
    values.push(value);
  }
  return values;
}

function cmdModeFacade(argv, a) {
  const [profile] = leadingPositionals(argv);
  const scope = a.workspace ? "workspace" : a.global ? "global" : (profile ? "global" : "effective");
  if (a.reset) {
    cmdConfig({ action: "reset", scope: scope === "effective" ? "workspace" : scope, store_path: a.store_path, output: a.output });
    return;
  }
  if (!profile) {
    cmdConfig({ action: "show", scope, store_path: a.store_path, output: a.output });
    return;
  }
  cmdConfig({ action: "set", profile, scope, store_path: a.store_path, output: a.output });
}

function cmdRememberFacade(argv, a) {
  const positional = leadingPositionals(argv);
  let type = "decision";
  if (VALID_TYPES.includes(positional[0])) type = positional.shift();
  const title = a.title || positional.shift();
  const summary = a.summary || positional.join(" ");
  const scope = a.global ? "global" : "workspace";
  const visibility = a.private ? "private" : (scope === "global" ? "global" : "shared");
  cmdStore({
    ...a,
    type,
    title,
    summary,
    scope,
    visibility,
    intent: a.auto ? "automatic" : "explicit",
  });
}

function cmdRecallFacade(argv, a) {
  const value = a.id || a.query || leadingPositionals(argv).join(" ");
  requireNonEmpty(value, "query-or-id");
  if (a.id || /^mem_/.test(value)) {
    cmdRecall({ ...a, id: value, scope: a.scope || "all" });
    return;
  }
  cmdSearch({ ...a, query: value, scope: a.scope || "all", limit: a.limit || 5, intent: a.auto ? "automatic" : "explicit" });
}

function statusSnapshot(a = {}) {
  const profile = effectiveMemoryConfig("workspace", a.store_path);
  const paths = {
    global: resolveStorePath(a.store_path, "global"),
    workspace: resolveStorePath(a.store_path, "workspace"),
  };
  const counts = { global: 0, workspace: 0, total: 0 };
  for (const scope of ["global", "workspace"]) {
    counts[scope] = loadMemories(paths[scope]).filter((m) => canAccessMemory(defaults(m, scope), agentIdentity(a))).length;
    counts.total += counts[scope];
  }
  return { version: packageVersion(), profile, paths, memories: counts };
}

function cmdStatusFacade(a) {
  const snapshot = statusSnapshot(a);
  if (a.json || a.stdout || a.output) {
    writeOutput(snapshot, a.output);
    return;
  }
  process.stdout.write(
    `Memory Store v${snapshot.version}\n` +
    `Mode: ${snapshot.profile.profile} (${snapshot.profile.source})\n` +
    `Memories: ${snapshot.memories.total} (workspace ${snapshot.memories.workspace}, global ${snapshot.memories.global})\n` +
    `Workspace: ${snapshot.paths.workspace}\n` +
    `Global: ${snapshot.paths.global}\n`
  );
}

function maintenancePreview(a = {}) {
  const scope = validateScope(a.scope || "all", { allowAll: true });
  const now = Date.now();
  let active = 0;
  let candidates = 0;
  for (const [scopeName, storePath] of resolveTargetPaths(a.store_path, scope)) {
    for (let memory of loadMemories(storePath)) {
      memory = defaults(memory, scopeName);
      if (!canAccessMemory(memory, agentIdentity(a))) continue;
      active++;
      const created = new Date(memory.created_at).getTime();
      const ageDays = Number.isFinite(created) ? Math.max(0, (now - created) / 86400000) : 0;
      const ttlExpired = Boolean(memory.ttl_days && ageDays >= memory.ttl_days);
      const decayed = computeDecay(memory) < Number(a.min_decay ?? 0.15);
      if (ttlExpired || decayed) candidates++;
    }
  }
  return { applied: false, scope, active, candidates };
}

function cmdMaintainFacade(a) {
  const preview = maintenancePreview(a);
  if (a.apply) {
    process.stdout.write(`Maintenance summary: ${preview.candidates} candidate(s) across ${preview.active} active memories.\n`);
    cmdArchive({ ...a, scope: preview.scope, apply_decay: true });
    return;
  }
  if (a.json || a.stdout || a.output) {
    writeOutput(preview, a.output);
    return;
  }
  process.stdout.write(
    `Maintenance preview: ${preview.candidates} archive candidate(s) across ${preview.active} active memories.\n` +
    "No changes were made. Run `memory-store maintain --apply` to apply safe archiving.\n"
  );
}

async function cmdSetupFacade(argv, a) {
  const installerArgs = [];
  if (!a.sync && !a.check && !a.list && !a.help && !a.all && !a.agent && !a.target) {
    fail("setup requires --agent, --target, or --all. Run `memory-store` for the guided setup menu.");
  }
  if (a.sync) installerArgs.push("--update");
  if (a.check) installerArgs.push("--check");
  if (a.list) installerArgs.push("--list");
  if (a.dry_run) installerArgs.push("--dry-run");
  if (a.all) installerArgs.push("--all");
  if (a.agent) installerArgs.push("--agent", a.agent);
  if (a.target) installerArgs.push("--target", a.target);
  if (a.mode) installerArgs.push("--memory-profile", a.mode);
  if (a.help) installerArgs.push("--help");
  await require("./install.js").main(installerArgs);
}

function interactiveStatus(write) {
  const snapshot = statusSnapshot();
  write(
    `\nMemory Store v${snapshot.version}\n` +
    `Current mode: ${snapshot.profile.profile} (${snapshot.profile.source})\n` +
    `Memories: ${snapshot.memories.total} (workspace ${snapshot.memories.workspace}, global ${snapshot.memories.global})\n` +
    `Workspace: ${snapshot.paths.workspace}\n` +
    `Global: ${snapshot.paths.global}\n`
  );
}

async function interactiveSetup(ask, write) {
  write("\nQuick setup\n  1. Install to an Agent\n  2. Sync an existing installation\n  0. Back\n");
  const action = await ask("Choose [0-2]: ");
  if (action === "0" || !["1", "2"].includes(action)) return;
  const agentChoices = [
    ["codex", "Codex"], ["claude", "Claude Code"], ["gemini", "Gemini CLI"],
    ["opencode", "OpenCode"], ["workbuddy", "WorkBuddy"], ["cursor", "Cursor"],
    ["windsurf", "Windsurf"], ["qoderworkcn", "QoderWorkCN"], ["trae-cn", "Trae CN"],
  ];
  write("Agent platform:\n");
  agentChoices.forEach(([, label], index) => write(`  ${index + 1}. ${label}\n`));
  const selectedAgent = await ask("Choose [1-9]: ");
  const target = agentChoices[Number(selectedAgent) - 1]?.[0];
  if (!target) {
    write("Setup cancelled: choose a listed Agent platform.\n");
    return;
  }
  let profile = null;
  if (action === "1") {
    write("Memory mode: 1. explicit (recommended)  2. balanced  3. proactive  4. off\n");
    const selected = await ask("Choose [1-4] (default 1): ");
    profile = ({ "1": "explicit", "2": "balanced", "3": "proactive", "4": "off" })[selected || "1"] || "explicit";
  }
  write(
    `\nSetup summary\n- Action: ${action === "1" ? "install" : "sync local package"}\n` +
    `- Agent: ${target}\n${profile ? `- Memory mode: ${profile}\n` : ""}` +
    "- Network access: none\n"
  );
  const confirmed = await ask("Proceed? [y/N]: ");
  if (confirmed.toLowerCase() !== "y") {
    write("Setup cancelled.\n");
    return;
  }
  const args = ["setup", "--agent", target];
  if (action === "2") args.push("--sync");
  if (profile) args.push("--mode", profile);
  await cmdSetupFacade(args, parseArgs(args.slice(1)));
}

async function interactiveSearch(ask, write) {
  const query = (await ask("\nSearch query: ")).trim();
  if (!query) {
    write("Search cancelled.\n");
    return;
  }
  write("Scope: 1. all  2. workspace  3. global\n");
  const scope = ({ "2": "workspace", "3": "global" })[await ask("Choose [1-3] (default 1): ")] || "all";
  const results = searchMemories({ query, scope, limit: 5, intent: "explicit" });
  if (!results.length) {
    write("No matching memories.\n");
    return;
  }
  write("\nResults:\n");
  results.forEach((memory, index) => write(`  ${index + 1}. ${memory.title} [${memory.type}]\n     ${memory.summary}\n`));
}

async function interactiveRemember(ask, write) {
  write("\nMemory type: 1. decision  2. preference  3. workflow  4. debug solution  5. fact\n");
  const type = ({ "2": "preference", "3": "workflow", "4": "debug_solution", "5": "fact" })[
    await ask("Choose [1-5] (default 1): ")
  ] || "decision";
  const title = (await ask("Title: ")).trim();
  const summary = (await ask("Summary: ")).trim();
  if (!title || !summary) {
    write("Add cancelled: title and summary are required.\n");
    return;
  }
  write("Store in: 1. current workspace (shared)  2. global  3. current workspace (private)\n");
  const destination = await ask("Choose [1-3] (default 1): ");
  const scope = destination === "2" ? "global" : "workspace";
  const visibility = destination === "3" ? "private" : (scope === "global" ? "global" : "shared");
  let agentId = process.env.MEMORY_AGENT_ID || null;
  if (visibility === "private" && !agentId) agentId = (await ask("Agent ID for private access: ")).trim();
  write(
    `\nMemory summary\n- Type: ${type}\n- Title: ${title}\n- Scope: ${scope}\n` +
    `- Visibility: ${visibility}\n- Data path: ${resolveStorePath(null, scope)}\n`
  );
  const confirmed = await ask("Save this memory? [y/N]: ");
  if (confirmed.toLowerCase() !== "y") {
    write("Add cancelled.\n");
    return;
  }
  if (visibility === "private" && !agentId) {
    write("Add cancelled: private memories require an Agent ID.\n");
    return;
  }
  cmdStore({ type, title, summary, scope, visibility, agent_id: agentId, intent: "explicit" });
}

async function interactiveMode(ask, write) {
  const current = effectiveMemoryConfig("workspace");
  write(`\nCurrent mode: ${current.profile} (${current.source})\nApply to:\n  1. Current workspace\n  2. Global default\n  3. Remove workspace override\n  0. Back\n`);
  const target = await ask("Choose [0-3]: ");
  if (target === "0" || !["1", "2", "3"].includes(target)) return;
  if (target === "3") {
    const configPath = path.join(resolveStorePath(null, "workspace"), "config.json");
    write(`\nChange summary\n- Remove workspace override: ${configPath}\n`);
    if ((await ask("Apply change? [y/N]: ")).toLowerCase() !== "y") {
      write("Change cancelled.\n");
      return;
    }
    if (fs.existsSync(configPath)) fs.unlinkSync(configPath);
    write("Workspace override removed.\n");
    return;
  }
  write("Mode: 1. off  2. explicit  3. balanced  4. proactive\n");
  const profile = ({ "1": "off", "2": "explicit", "3": "balanced", "4": "proactive" })[
    await ask("Choose [1-4]: ")
  ];
  if (!profile) {
    write("Change cancelled.\n");
    return;
  }
  const scope = target === "1" ? "workspace" : "global";
  write(`\nChange summary\n- Scope: ${scope}\n- Mode: ${profile}\n- Path: ${path.join(resolveStorePath(null, scope), "config.json")}\n`);
  if ((await ask("Apply change? [y/N]: ")).toLowerCase() !== "y") {
    write("Change cancelled.\n");
    return;
  }
  writeMemoryConfig(scope, null, profile);
  write(`Memory mode changed to ${profile} for ${scope}.\n`);
}

async function interactiveMaintenance(ask, write) {
  const preview = maintenancePreview({ scope: "all" });
  write(
    `\nMaintenance preview\n- Active memories: ${preview.active}\n` +
    `- Archive candidates: ${preview.candidates}\n- No changes have been made.\n`
  );
  if (!preview.candidates) return;
  if ((await ask("Apply safe archive? [y/N]: ")).toLowerCase() !== "y") {
    write("Maintenance cancelled.\n");
    return;
  }
  write(`Maintenance summary: archive ${preview.candidates} candidate(s) from both stores.\n`);
  cmdArchive({ scope: "all", apply_decay: true });
}

async function runInteractive({ ask, write = (text) => process.stdout.write(text) }) {
  write("\nMemory Store\n");
  while (true) {
    write(
      "\n1. Quick setup\n2. Search memories\n3. Add a memory\n" +
      "4. Change memory mode\n5. View status\n6. Maintenance preview\n0. Exit\n"
    );
    const choice = (await ask("Choose [0-6]: ")).trim();
    if (choice === "0") {
      write("Goodbye.\n");
      return;
    }
    if (choice === "1") await interactiveSetup(ask, write);
    else if (choice === "2") await interactiveSearch(ask, write);
    else if (choice === "3") await interactiveRemember(ask, write);
    else if (choice === "4") await interactiveMode(ask, write);
    else if (choice === "5") interactiveStatus(write);
    else if (choice === "6") await interactiveMaintenance(ask, write);
    else write("Choose a number from 0 to 6.\n");
  }
}

async function runTerminalMenu() {
  const readline = require("readline");
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  let interrupted = false;
  let pendingResolve = null;
  rl.on("SIGINT", () => {
    interrupted = true;
    process.stdout.write("\n");
    if (pendingResolve) pendingResolve("0");
  });
  const ask = (question) => {
    if (interrupted) return Promise.resolve("0");
    return new Promise((resolve) => {
      pendingResolve = resolve;
      rl.question(question, (answer) => {
        pendingResolve = null;
        resolve(answer);
      });
    });
  };
  try {
    await runInteractive({ ask });
  } finally {
    rl.close();
  }
}

// ==============================================================================
// CLI parser & main
// ==============================================================================

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2).replace(/-/g, "_"); // --store-path -> store_path
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith("--")) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

function printCompactHelp() {
  process.stdout.write(
    "Memory Store — run without arguments in a terminal for the guided menu.\n" +
    "Usage: memory-store <command> [options]\n" +
    "  remember   Add a memory with safe defaults\n" +
    "  recall     Search memories or open one by ID\n" +
    "  mode       View or change the memory profile\n" +
    "  status     Show profile, paths, and counts\n" +
    "  setup      Install or sync the skill explicitly\n" +
    "  maintain   Preview maintenance candidates\n" +
    "Run `memory-store help --advanced` for the compatible low-level commands.\n"
  );
}

function printAdvancedHelp() {
  process.stdout.write(
    "Memory Store advanced commands (v1 compatible):\n" +
    "  init config store search recall list update delete merge archive restore revive stats compress migrate version\n" +
    "Usage: memory-store <command> [--key value ...]\n" +
    "Output defaults to stdout; use --output <file> to write JSON to a file.\n" +
    "Docs: see references/cli.md relative to the skill directory.\n"
  );
}

async function main(argv = process.argv.slice(2)) {
  if (argv.length === 0 || argv[0] === "--help" || argv[0] === "-h" || argv[0] === "help") {
    if (argv.length === 0 && process.stdin.isTTY && process.stdout.isTTY) {
      await runTerminalMenu();
      return;
    }
    if (argv.includes("--advanced")) printAdvancedHelp();
    else printCompactHelp();
    return;
  }
  if (argv[0] === "--version" || argv[0] === "-v" || argv[0] === "version") {
    cmdVersion(parseArgs(argv.slice(1)));
    return;
  }
  const command = argv[0];
  const a = parseArgs(argv.slice(1));
  if (command === "config" && argv[1] && !argv[1].startsWith("--")) a.action = argv[1];
  // --stdout forces JSON to stdout (no file). Output already defaults to stdout
  // when --output is omitted; this makes the intent explicit.
  if (a.stdout) delete a.output;
  if (command === "mode") return cmdModeFacade(argv, a);
  if (command === "remember") return cmdRememberFacade(argv, a);
  if (command === "recall" && !a.id && !argv.slice(1).some((value) => value === "--id")) {
    return cmdRecallFacade(argv, a);
  }
  if (command === "status") return cmdStatusFacade(a);
  if (command === "maintain") return cmdMaintainFacade(a);
  if (command === "setup") return cmdSetupFacade(argv, a);
  const handlers = {
    init: cmdInit,
    config: cmdConfig,
    store: cmdStore,
    search: cmdSearch,
    recall: cmdRecall,
    list: cmdList,
    update: cmdUpdate,
    delete: cmdDelete,
    merge: cmdMerge,
    archive: cmdArchive,
    restore: cmdRestore,
    revive: cmdRestore,
    stats: cmdStats,
    compress: cmdCompress,
    migrate: cmdMigrate,
    version: cmdVersion,
  };
  if (!handlers[command]) {
    process.stderr.write(`Error: Unknown command '${command}'\n`);
    process.exit(1);
  }
  handlers[command](a);
}

if (require.main === module) {
  main().catch((error) => {
    process.stderr.write(`Error: ${error.message}\n`);
    process.exitCode = 1;
  });
}

module.exports = { main, runInteractive };
