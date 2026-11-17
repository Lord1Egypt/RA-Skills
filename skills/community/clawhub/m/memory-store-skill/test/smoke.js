#!/usr/bin/env node
"use strict";

/**
 * Smoke test for memory_cli.js — exercises the core CLI surface against a
 * throwaway store directory. Run with: node test/smoke.js  (or npm test).
 *
 * No external deps: uses only Node built-ins.
 */

const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const assert = require("assert");

const CLI = path.resolve(__dirname, "..", "scripts", "memory_cli.js");
const NODE = process.execPath;

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "memory-smoke-"));
const STORE = path.join(TMP, "store");
const OUT = path.join(TMP, "out");
fs.mkdirSync(OUT, { recursive: true });

let passed = 0;
let failed = 0;

function run(args) {
  return execFileSync(NODE, [CLI, ...args], { encoding: "utf8" });
}

function runJson(args) {
  const out = path.join(OUT, `r_${Math.random().toString(36).slice(2)}.json`);
  run([...args, "--output", out]);
  return JSON.parse(fs.readFileSync(out, "utf8"));
}

function runFails(args) {
  try {
    run(args);
    return false;
  } catch (e) {
    return e.status !== 0;
  }
}

function check(name, cond, extra) {
  if (cond) {
    passed++;
    console.log(`  ✓ ${name}`);
  } else {
    failed++;
    console.error(`  ✗ ${name}${extra ? " — " + extra : ""}`);
  }
}

try {
  // --- init ---------------------------------------------------------------
  run(["init", "--scope", "global", "--store-path", STORE]);
  check("init creates memories.json", fs.existsSync(path.join(STORE, "memories.json")));

  // --- store --------------------------------------------------------------
  run([
    "store", "--type", "decision", "--title", "DB selection",
    "--summary", "Chose SQLite over Postgres", "--tags", "db,arch",
    "--importance", "0.9", "--store-path", STORE,
  ]);
  run([
    "store", "--type", "debug_solution", "--title", "Null pointer fix",
    "--summary", "Guard against null in parse", "--tags", "bug",
    "--importance", "0.7", "--store-path", STORE,
  ]);

  // --- list ---------------------------------------------------------------
  const list = runJson(["list", "--scope", "global", "--store-path", STORE]);
  check("list returns 2 memories", Array.isArray(list) && list.length === 2, `got ${list && list.length}`);

  // --- search (english keyword) ------------------------------------------
  const search = runJson(["search", "--query", "SQLite", "--scope", "global", "--store-path", STORE]);
  check("search finds decision by keyword", search.length >= 1 && search[0].type === "decision", `got ${search.length}`);

  // --- search (chinese n-gram) -------------------------------------------
  const searchCn = runJson(["search", "--query", "选择 SQLite", "--scope", "global", "--store-path", STORE]);
  check("chinese n-gram search hits", searchCn.length >= 1);

  // --- recall (access count increments) ----------------------------------
  const firstId = list.find((m) => m.type === "decision").id;
  const recalled = runJson(["recall", "--id", firstId, "--store-path", STORE]);
  check("recall returns memory + increments access", recalled.id === firstId && recalled.access_count === 1, `access=${recalled.access_count}`);

  // --- update -------------------------------------------------------------
  run(["update", "--id", firstId, "--visibility", "private", "--as-agent", "agent-a", "--store-path", STORE]);
  const afterUpdate = runJson(["list", "--scope", "global", "--as-agent", "agent-a", "--store-path", STORE]).find((m) => m.id === firstId);
  check("update changes visibility", afterUpdate && afterUpdate.visibility === "private");

  // --- visibility filter --------------------------------------------------
  const privOnly = runJson(["list", "--scope", "global", "--visibility", "private", "--as-agent", "agent-a", "--store-path", STORE]);
  check("visibility filter works", privOnly.length === 1 && privOnly[0].id === firstId);
  const anonymousList = runJson(["list", "--scope", "global", "--store-path", STORE]);
  check("anonymous list excludes private memories", anonymousList.every((m) => m.id !== firstId));
  const anonymousSearch = runJson(["search", "--query", "SQLite", "--scope", "global", "--store-path", STORE]);
  check("anonymous search excludes private memories", anonymousSearch.every((m) => m.id !== firstId));
  const otherSearch = runJson(["search", "--query", "SQLite", "--scope", "global", "--as-agent", "agent-b", "--store-path", STORE]);
  check("other agent search excludes private memories", otherSearch.every((m) => m.id !== firstId));
  check("anonymous recall denies private memory", runFails(["recall", "--id", firstId, "--store-path", STORE]));
  const ownerRecall = runJson(["recall", "--id", firstId, "--as-agent", "agent-a", "--store-path", STORE]);
  check("owner can recall private memory", ownerRecall.id === firstId);
  check("other agent cannot update private memory", runFails(["update", "--id", firstId, "--summary", "nope", "--as-agent", "agent-b", "--store-path", STORE]));
  check("other agent cannot delete private memory", runFails(["delete", "--id", firstId, "--as-agent", "agent-b", "--store-path", STORE]));

  // --- stats --------------------------------------------------------------
  const stats = runJson(["stats", "--scope", "global", "--as-agent", "agent-a", "--store-path", STORE]);
  check("stats totals 2", stats.total_memories === 2, `got ${stats.total_memories}`);
  check("stats type breakdown present", stats.type_breakdown && stats.type_breakdown.decision === 1);

  // --- migrate dry-run (must not throw, returns numbers) ------------------
  const mig = runJson(["migrate", "--dry-run", "--store-path", STORE]);
  check("migrate dry-run runs", mig && typeof mig.total_now === "number" && mig.dry_run === true);

  // --- --stdout emits pure JSON (no "Success!" line) ---------------------
  const stdoutOut = run(["search", "--query", "SQLite", "--scope", "global", "--store-path", STORE, "--stdout"]);
  let stdoutOk = false;
  try { JSON.parse(stdoutOut); stdoutOk = !/Success!/.test(stdoutOut); } catch (e) { stdoutOk = false; }
  check("--stdout emits pure JSON (no Success! line)", stdoutOk);

  // --- --type multi-value ------------------------------------------------
  const multiType = runJson(["search", "--query", "", "--type", "decision,debug_solution", "--scope", "global", "--as-agent", "agent-a", "--store-path", STORE]);
  check("--type multi-value returns both types", multiType.length === 2 && new Set(multiType.map((m) => m.type)).size === 2, `got ${multiType.length}`);

  // --- --type invalid -> non-zero exit -----------------------------------
  let typeErr = false;
  try {
    run(["search", "--query", "", "--type", "bogus", "--scope", "global", "--store-path", STORE, "--output", path.join(OUT, "x.json")]);
  } catch (e) {
    typeErr = e.status !== 0;
  }
  check("--type invalid exits non-zero", typeErr);

  // --- --output is a directory -> non-zero exit --------------------------
  const dirOut = path.join(OUT, "adir");
  fs.mkdirSync(dirOut);
  let dirErr = false;
  try {
    run(["list", "--scope", "global", "--store-path", STORE, "--output", dirOut]);
  } catch (e) {
    dirErr = e.status !== 0;
  }
  check("--output directory exits non-zero", dirErr);

  // --- compress generic chat format --------------------------------------
  const chatFile = path.join(OUT, "chat.jsonl");
  fs.writeFileSync(chatFile, JSON.stringify({ role: "user", content: "用什么数据库？" }) + "\n" + JSON.stringify({ role: "assistant", content: "用 SQLite" }) + "\n");
  const comp = runJson(["compress", "--input", chatFile]);
  check("compress generic-chat detected", comp.detected_format === "generic-chat" && comp.extracted_steps_count === 2, `fmt=${comp.detected_format}`);

  // --- input validation ---------------------------------------------------
  const INVALID = path.join(TMP, "invalid");
  check("store requires title", runFails(["store", "--type", "fact", "--summary", "x", "--store-path", INVALID]));
  check("store requires summary", runFails(["store", "--type", "fact", "--title", "x", "--store-path", INVALID]));
  check("store rejects invalid scope", runFails(["store", "--type", "fact", "--title", "x", "--summary", "x", "--scope", "bogus", "--store-path", INVALID]));
  check("store rejects invalid visibility", runFails(["store", "--type", "fact", "--title", "x", "--summary", "x", "--visibility", "secret", "--store-path", INVALID]));
  check("store rejects invalid priority", runFails(["store", "--type", "fact", "--title", "x", "--summary", "x", "--priority", "P0", "--store-path", INVALID]));
  check("store rejects out-of-range importance", runFails(["store", "--type", "fact", "--title", "x", "--summary", "x", "--importance", "2", "--store-path", INVALID]));
  check("store rejects non-positive TTL", runFails(["store", "--type", "fact", "--title", "x", "--summary", "x", "--ttl-days", "0", "--store-path", INVALID]));
  check("private store requires an owner identity", runFails(["store", "--type", "fact", "--title", "x", "--summary", "x", "--visibility", "private", "--store-path", INVALID]));
  check("search rejects non-positive limit", runFails(["search", "--query", "x", "--limit", "0", "--store-path", STORE]));
  check("list rejects fractional limit", runFails(["list", "--limit", "1.5", "--store-path", STORE]));
  check("list rejects invalid visibility filter", runFails(["list", "--visibility", "secret", "--store-path", STORE]));

  // --- corrupted JSON must fail closed -----------------------------------
  const CORRUPT = path.join(TMP, "corrupt");
  fs.mkdirSync(CORRUPT, { recursive: true });
  const corruptFile = path.join(CORRUPT, "memories.json");
  fs.writeFileSync(corruptFile, "{not-json", "utf8");
  check("corrupted main store rejects writes", runFails(["store", "--type", "fact", "--title", "safe", "--summary", "safe", "--store-path", CORRUPT]));
  check("corrupted main store is preserved", fs.readFileSync(corruptFile, "utf8") === "{not-json");

  // --- merge preserves semantic scope ------------------------------------
  const MERGE = path.join(TMP, "merge");
  run(["store", "--type", "fact", "--title", "one", "--summary", "one", "--scope", "workspace", "--store-path", MERGE]);
  run(["store", "--type", "fact", "--title", "two", "--summary", "two", "--scope", "workspace", "--store-path", MERGE]);
  const mergeList = runJson(["list", "--scope", "workspace", "--store-path", MERGE]);
  const merged = runJson(["merge", "--ids", mergeList.map((m) => m.id).join(","), "--scope", "workspace", "--store-path", MERGE]);
  check("merge stores workspace scope, not filesystem path", merged.scope === "workspace", `scope=${merged.scope}`);

  // --- decay priority order ----------------------------------------------
  const DECAY = path.join(TMP, "decay");
  for (const priority of ["P1", "P2", "P3"]) {
    run(["store", "--type", "fact", "--title", priority, "--summary", `${priority} decay`, "--priority", priority, "--importance", "0.9", "--store-path", DECAY]);
  }
  const decayFile = path.join(DECAY, "memories.json");
  const decaySeed = JSON.parse(fs.readFileSync(decayFile, "utf8"));
  const weekAgo = new Date(Date.now() - 7 * 86400000).toISOString();
  for (const m of decaySeed) m.created_at = weekAgo;
  fs.writeFileSync(decayFile, JSON.stringify(decaySeed, null, 2) + "\n", "utf8");
  run(["archive", "--scope", "global", "--apply-decay", "--min-decay", "0", "--store-path", DECAY]);
  const decayed = runJson(["list", "--scope", "global", "--store-path", DECAY]);
  const decayByPriority = Object.fromEntries(decayed.map((m) => [m.priority, m.decay_score]));
  check("decay order is P1 > P2 > P3", decayByPriority.P1 > decayByPriority.P2 && decayByPriority.P2 > decayByPriority.P3, JSON.stringify(decayByPriority));

  // --- search remains read-only unless --touch ---------------------------
  const TOUCH = path.join(TMP, "touch");
  run(["store", "--type", "fact", "--title", "touch target", "--summary", "search touch behavior", "--store-path", TOUCH]);
  const touchId = runJson(["list", "--store-path", TOUCH])[0].id;
  runJson(["search", "--query", "touch", "--store-path", TOUCH]);
  const untouched = runJson(["list", "--store-path", TOUCH])[0];
  check("search without --touch is read-only", untouched.id === touchId && untouched.access_count === 0);
  const touchedResult = runJson(["search", "--query", "touch", "--touch", "--store-path", TOUCH]);
  const touched = runJson(["list", "--store-path", TOUCH])[0];
  check("search --touch increments selected hits", touchedResult[0].access_count === 1 && touched.access_count === 1 && Boolean(touched.last_accessed));

  const PRIVATE_DELETE = path.join(TMP, "private-delete");
  run(["store", "--type", "fact", "--title", "owned", "--summary", "private", "--visibility", "private", "--agent-id", "agent-a", "--store-path", PRIVATE_DELETE]);
  const privateDeleteId = runJson(["list", "--as-agent", "agent-a", "--store-path", PRIVATE_DELETE])[0].id;
  run(["delete", "--id", privateDeleteId, "--as-agent", "agent-a", "--store-path", PRIVATE_DELETE]);
  check("owner can delete private memory", runJson(["list", "--as-agent", "agent-a", "--store-path", PRIVATE_DELETE]).length === 0);

  // --- archive all + archived list/recall/restore ------------------------
  const LAYERS = path.join(TMP, "layers");
  const GLOBAL_LAYER = path.join(LAYERS, "global");
  const WORKSPACE_LAYER = path.join(LAYERS, "workspace");
  run(["store", "--type", "state", "--title", "global old", "--summary", "archive me", "--importance", "0.1", "--scope", "global", "--store-path", GLOBAL_LAYER]);
  run(["store", "--type", "state", "--title", "workspace old", "--summary", "archive me", "--importance", "0.1", "--scope", "workspace", "--store-path", WORKSPACE_LAYER]);
  const archivedAll = runJson(["archive", "--scope", "all", "--min-importance", "0.5", "--store-path", LAYERS]);
  check("archive --scope all covers both layers", archivedAll.length === 2 && new Set(archivedAll.map((m) => m.scope)).size === 2, `got ${archivedAll.length}`);
  const archivedList = runJson(["list", "--scope", "all", "--status", "archived", "--store-path", LAYERS]);
  check("list --status archived reads archive files", archivedList.length === 2 && archivedList.every((m) => m.status === "archived"));
  const archivedId = archivedList.find((m) => m.scope === "workspace").id;
  const archivedRecall = runJson(["recall", "--id", archivedId, "--scope", "all", "--store-path", LAYERS]);
  check("recall reads and touches archived memory", archivedRecall.status === "archived" && archivedRecall.access_count === 1);
  const restored = runJson(["restore", "--id", archivedId, "--scope", "all", "--store-path", LAYERS]);
  check("restore moves archived memory back to active", restored.status === "active" && restored.id === archivedId);
  const archivedAfterRestore = runJson(["list", "--scope", "all", "--status", "archived", "--store-path", LAYERS]);
  check("restore removes source archive entry", archivedAfterRestore.length === 1 && archivedAfterRestore[0].id !== archivedId);

  // Bulk archive preserves private memories unless the owner identity is supplied.
  const PRIVATE_ARCHIVE = path.join(TMP, "private-archive");
  run(["store", "--type", "state", "--title", "public old", "--summary", "archive me", "--importance", "0.1", "--store-path", PRIVATE_ARCHIVE]);
  run(["store", "--type", "state", "--title", "private old", "--summary", "owner only", "--importance", "0.1", "--visibility", "private", "--agent-id", "agent-a", "--store-path", PRIVATE_ARCHIVE]);
  const anonymousArchive = runJson(["archive", "--scope", "global", "--min-importance", "0.5", "--store-path", PRIVATE_ARCHIVE]);
  const privateStillActive = runJson(["list", "--scope", "global", "--as-agent", "agent-a", "--store-path", PRIVATE_ARCHIVE]);
  check("anonymous archive preserves private memories", anonymousArchive.length === 1 && privateStillActive.length === 1 && privateStillActive[0].visibility === "private");
  const ownerArchive = runJson(["archive", "--scope", "global", "--min-importance", "0.5", "--as-agent", "agent-a", "--store-path", PRIVATE_ARCHIVE]);
  check("owner can archive private memories", ownerArchive.length === 1 && ownerArchive[0].visibility === "private");

  // A corrupt archive in another store does not affect explicitly scoped reads.
  const BAD_ARCHIVE_STORE = path.join(TMP, "bad-archive");
  const BAD_ARCHIVE_DIR = path.join(BAD_ARCHIVE_STORE, "archive");
  fs.mkdirSync(BAD_ARCHIVE_DIR, { recursive: true });
  fs.writeFileSync(path.join(BAD_ARCHIVE_STORE, "memories.json"), "[]\n", "utf8");
  fs.writeFileSync(path.join(BAD_ARCHIVE_DIR, "archived_200001.json"), "{broken", "utf8");
  check("corrupted archive fails closed when read", runFails(["list", "--scope", "global", "--status", "archived", "--store-path", BAD_ARCHIVE_STORE]));
  const healthyScoped = runJson(["list", "--scope", "global", "--store-path", GLOBAL_LAYER]);
  check("corrupted archive does not block unrelated scoped active list", Array.isArray(healthyScoped));

  // --- archive (decay threshold removes low-value) — run last (destructive) ---
  run(["archive", "--scope", "global", "--apply-decay", "--min-decay", "1.0", "--store-path", STORE]);
  const afterArchive = runJson(["list", "--scope", "global", "--store-path", STORE]);
  check("archive removes by decay threshold", afterArchive.length < list.length, `remaining ${afterArchive.length}`);

  // --- version subcommand / -v flag --------------------------------------
  const verOut = run(["version"]).trim();
  check("version subcommand prints version", /^memory-store v\d+\.\d+\.\d+/.test(verOut), verOut);
  const verFlag = run(["-v"]).trim();
  check("-v flag prints version", /^memory-store v\d+\.\d+\.\d+/.test(verFlag), verFlag);

  // --- unknown command exits non-zero ------------------------------------
  let errored = false;
  try {
    run(["bogus-cmd"]);
  } catch (e) {
    errored = e.status !== 0;
  }
  check("unknown command exits non-zero", errored);
} catch (e) {
  failed++;
  console.error("FATAL:", e.stack || e.message);
}

console.log(`\nSmoke test: ${passed} passed, ${failed} failed`);
fs.rmSync(TMP, { recursive: true, force: true });
process.exit(failed ? 1 : 0);
