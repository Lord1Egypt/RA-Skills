/**
 * OpenMem - Bootstrap Hook
 *
 * Injects long-term memories into the agent context at session start.
 * Fires on agent:bootstrap before workspace files are loaded.
 *
 * Reads from openmem-cache.json — a plain JSON file written by mem.py
 * and mcp_server.py after every memory write. No process spawning required.
 *
 * Compression is on-demand only — say "compress my sessions" or "save to memory".
 */

"use strict";

const path = require("path");
const os = require("os");
const fs = require("fs");

const DEFAULT_DB_DIR = path.join(os.homedir(), ".openclaw", "workspace", "memory");
const DB_DIR = process.env.OPENMEM_DB
  ? path.dirname(process.env.OPENMEM_DB)
  : DEFAULT_DB_DIR;
const CACHE_FILE = path.join(DB_DIR, "openmem-cache.json");
const INJECT_LIMIT = parseInt(process.env.OPENMEM_BOOTSTRAP_LIMIT || "12", 10);

function loadCache() {
  try {
    const raw = fs.readFileSync(CACHE_FILE, "utf8");
    const cache = JSON.parse(raw);
    if (!Array.isArray(cache.memories)) return null;
    return cache.memories.slice(0, INJECT_LIMIT);
  } catch {
    // Cache doesn't exist yet or is unreadable — not an error
    return null;
  }
}

function formatMemories(memories) {
  if (!memories || memories.length === 0) return null;

  const lines = [
    "## Long-Term Memory (OpenMem)",
    "",
    "Memories from previous sessions (highest importance first):",
    "",
  ];

  for (const mem of memories) {
    const cat = mem.category || "general";
    const imp = typeof mem.importance === "number" ? mem.importance.toFixed(1) : "0.5";
    const content = (mem.content || "").trim();
    if (!content) continue;
    lines.push(`**[${cat}]** (importance: ${imp})`);
    lines.push(content);
    lines.push("");
  }

  lines.push("---");
  lines.push("*Tools: memory_add · memory_search · memory_update · memory_delete · memory_list · memory_stats*");

  return lines.join("\n");
}

const handler = async (event) => {
  if (!event || typeof event !== "object") return;
  if (event.type !== "agent" || event.action !== "bootstrap") return;
  if (!event.context || !Array.isArray(event.context.bootstrapFiles)) return;

  // Skip sub-agent sessions
  const sessionKey = event.sessionKey || "";
  if (sessionKey.includes(":subagent:")) return;

  const memories = loadCache();
  if (!memories || memories.length === 0) return;

  const content = formatMemories(memories);
  if (!content) return;

  event.context.bootstrapFiles.push({
    path: "OPENMEM.md",
    content,
    virtual: true,
  });
};

module.exports = handler;
module.exports.default = handler;
