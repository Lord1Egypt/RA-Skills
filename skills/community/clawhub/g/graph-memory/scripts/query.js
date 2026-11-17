#!/usr/bin/env node
/**
 * graph-memory skill — query.js
 * ─────────────────────────────────────────────
 * OpenClaw skill wrapper around the knowledge graph.
 * Exports three functions that return markdown strings:
 *   graph_search(query, options)
 *   graph_stats()
 *   graph_related(entity, depth)
 *
 * Reuses query-bridge.cjs via require() when better-sqlite3 is available.
 * Falls back to direct sqlite3 async queries when better-sqlite3 is missing.
 * Prepared statements are cached in an LRU (capacity 10).
 */

const fs = require("fs");
const path = require("path");

/* ── Paths ───────────────────────────────────── */
const DB_PATH = path.join(
  process.env.HOME,
  ".openclaw",
  "workspace",
  ".openclaw_memory",
  "graph.db"
);
const BRIDGE_PATH = path.join(
  process.env.HOME,
  ".openclaw",
  "workspace",
  "code",
  "graph-memory",
  "scripts",
  "query-bridge.cjs"
);

/* ── Load query-bridge.cjs (best-effort) ─────── */
let queryBridge = null;
let bridgeDb = null;
let bridgeMode = "none";

try {
  const mod = require(BRIDGE_PATH);
  queryBridge = mod.queryBridge;
  if (queryBridge && queryBridge.db) {
    bridgeDb = queryBridge.db;
    // query-bridge.cjs sets its own dbMode internally; we probe it
    bridgeMode = "bridge";
  }
} catch (e) {
  // bridge failed to load (likely better-sqlite3 missing)
}

/* ── Direct DB connection (fallback) ─────────── */
let db = null;
let dbMode = "none";

function initDb() {
  if (db) return; // already initialized

  if (!fs.existsSync(DB_PATH)) return;

  // Prefer better-sqlite3 (sync, fast)
  try {
    const Database = require("better-sqlite3");
    db = new Database(DB_PATH);
    dbMode = "better-sqlite3";
    return;
  } catch (_) {
    // fall through
  }

  // Fallback: sqlite3 (async)
  try {
    const sqlite3 = require("sqlite3");
    db = new sqlite3.Database(DB_PATH);
    dbMode = "sqlite3";
  } catch (_) {
    // neither driver available
  }
}

/* ── Statement Cache (LRU, capacity 10) ──────── */
class StatementCache {
  constructor(capacity = 10) {
    this.capacity = capacity;
    this.cache = new Map(); // sql -> prepared Statement
  }

  get(sql) {
    if (!db || dbMode !== "better-sqlite3") return null;
    if (this.cache.has(sql)) {
      // touch (move to end = most recently used)
      const stmt = this.cache.get(sql);
      this.cache.delete(sql);
      this.cache.set(sql, stmt);
      return stmt;
    }
    try {
      const stmt = db.prepare(sql);
      if (this.cache.size >= this.capacity) {
        const oldest = this.cache.keys().next().value;
        this.cache.delete(oldest);
      }
      this.cache.set(sql, stmt);
      return stmt;
    } catch (e) {
      return null;
    }
  }

  clear() {
    this.cache.clear();
  }
}

const stmtCache = new StatementCache(10);

/* ── Low-level DB helpers ────────────────────── */

/** Execute SELECT … ALL with optional statement caching */
function dbAll(sql, params = []) {
  // Try cache first
  const cached = stmtCache.get(sql);
  if (cached) {
    try {
      return cached.all(...params);
    } catch (_) {
      /* fallback to uncached */
    }
  }

  if (dbMode === "better-sqlite3") {
    return db.prepare(sql).all(...params);
  }
  if (dbMode === "sqlite3") {
    return new Promise((resolve, reject) => {
      db.all(sql, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  }
  return [];
}

/** Execute SELECT … GET (single row) */
function dbGet(sql, params = []) {
  const cached = stmtCache.get(sql);
  if (cached) {
    try {
      return cached.get(...params);
    } catch (_) {
      /* fallback */
    }
  }

  if (dbMode === "better-sqlite3") {
    return db.prepare(sql).get(...params);
  }
  if (dbMode === "sqlite3") {
    return new Promise((resolve, reject) => {
      db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }
  return null;
}

/* ── Health check ────────────────────────────── */
function checkHealth() {
  if (!fs.existsSync(DB_PATH)) {
    return {
      ok: false,
      error: `Graph memory database not found at \`${DB_PATH}\``,
    };
  }
  initDb();
  if (!db && !bridgeDb) {
    return {
      ok: false,
      error:
        "Graph memory database exists but no SQLite driver is available. " +
        "Install `better-sqlite3` or `sqlite3`.",
    };
  }
  return { ok: true };
}

/* ── Entity enrichment helper ────────────────── */

/** Convert a raw DB row to the shape expected by fmtEntityList */
function enrichRow(row, deep) {
  const enriched = {
    name: row.name,
    type: row.entity_type,
    mentions: row.mention_count,
    firstSeen: row.first_seen,
    lastSeen: row.last_seen,
    description: row.description,
    neighbors: null,
  };

  if (deep && queryBridge) {
    try {
      enriched.neighbors = queryBridge._getNeighbors(row.name);
    } catch (_) {
      enriched.neighbors = null;
    }
  }

  return enriched;
}

/* ── Markdown formatters ─────────────────────── */

function fmtEntityList(query, results, deep) {
  let md = `## Graph Search: "${query}"\n\n`;
  md += `**${results.length}** entit${results.length !== 1 ? "ies" : "y"} found.\n\n`;

  const byType = {};
  for (const r of results) byType[r.type] = (byType[r.type] || 0) + 1;
  md += `**Types:** ${Object.entries(byType)
    .map(([t, c]) => `${t} (${c})`)
    .join(", ")}\n\n`;
  md += "---\n\n";

  for (const r of results) {
    md += `### ${r.name}\n`;
    md += `- **Type:** ${r.type}\n`;
    md += `- **Mentions:** ${r.mentions ?? 0}\n`;
    if (r.description) md += `- **Description:** ${r.description}\n`;
    if (r.firstSeen) md += `- **First seen:** ${r.firstSeen}\n`;
    if (r.lastSeen) md += `- **Last seen:** ${r.lastSeen}\n`;

    if (deep && r.neighbors) {
      const out = r.neighbors.outgoing?.length ?? 0;
      const inc = r.neighbors.incoming?.length ?? 0;
      if (out > 0 || inc > 0) {
        md += `- **Relationships:** ${out} outgoing, ${inc} incoming\n`;
        if (out > 0) {
          md += `  - Outgoing:\n`;
          for (const n of r.neighbors.outgoing.slice(0, 5)) {
            md += `    - → ${n.target ?? n.name} [${n.relation_type ?? "related"}]\n`;
          }
        }
        if (inc > 0) {
          md += `  - Incoming:\n`;
          for (const n of r.neighbors.incoming.slice(0, 5)) {
            md += `    - ← ${n.source ?? n.name} [${n.relation_type ?? "related"}]\n`;
          }
        }
      }
    }
    md += "\n";
  }
  return md.trim();
}

/* ── graph_search ────────────────────────────── */

/**
 * Search entities by text query.
 * @param {string} query
 * @param {object} [options]
 * @param {string} [options.type]   entity type filter
 * @param {boolean} [options.deep]  include neighbors
 * @param {number} [options.limit]  max results (default 20)
 * @returns {string} markdown
 */
function graph_search(query, options = {}) {
  const health = checkHealth();
  if (!health.ok) return health.error;

  const q = typeof query === "string" ? query.trim() : "";
  if (!q) return "Graph query error: query must be a non-empty string";

  try {
    const type = options.type || null;
    const deep = !!options.deep;
    const limit = Number.isFinite(options.limit) ? options.limit : 20;

    if (queryBridge) {
      try {
        const results = queryBridge.search(q, { type, limit, deep });
        if (results.length === 0) {
          return `No entities matching '${q}' found in graph memory.`;
        }
        return fmtEntityList(q, results, deep);
      } catch (e) {
        // FTS5 or other bridge errors — fall through to direct SQL
        if (!e.message || !e.message.includes("no such column")) {
          // Log unexpected errors for debugging (non-fatal)
          // eslint-disable-next-line no-console
          console.error("[graph-memory] queryBridge.search fallback:", e.message);
        }
      }
    }

    // Fallback: direct SQL (works for both better-sqlite3 and sqlite3)
    const pattern = `%${q}%`;
    let rows;

    if (queryBridge) {
      // Bridge loaded but FTS5 failed — use internal fuzzy search (no FTS)
      try {
        rows = queryBridge._fuzzySearch(q, type, limit);
      } catch (e) {
        rows = [];
      }
    } else {
      let sql;
      let params;
      if (type) {
        sql =
          "SELECT * FROM entities WHERE (name LIKE ? OR canonical_name LIKE ?) " +
          "AND entity_type = ? ORDER BY mention_count DESC LIMIT ?";
        params = [pattern, pattern, type, limit];
      } else {
        sql =
          "SELECT * FROM entities WHERE name LIKE ? OR canonical_name LIKE ? " +
          "ORDER BY mention_count DESC LIMIT ?";
        params = [pattern, pattern, limit];
      }
      rows = dbAll(sql, params);
    }

    // sqlite3 fallback returns a Promise — handle it
    if (rows && typeof rows.then === "function") {
      return rows
        .then((resolved) => {
          if (resolved.length === 0) {
            return `No entities matching '${q}' found in graph memory.`;
          }
          const results = resolved.map((r) => enrichRow(r, deep));
          return fmtEntityList(q, results, deep);
        })
        .catch((e) => `Graph query error: ${e.message}`);
    }

    if (rows.length === 0) {
      return `No entities matching '${q}' found in graph memory.`;
    }
    const results = rows.map((r) => enrichRow(r, deep));
    return fmtEntityList(q, results, deep);
  } catch (e) {
    return `Graph query error: ${e.message}`;
  }
}

/* ── graph_stats ─────────────────────────────── */

/**
 * Return graph statistics as markdown.
 * @returns {string|Promise<string>} markdown
 */
function graph_stats() {
  const health = checkHealth();
  if (!health.ok) return health.error;

  try {
    const entityCount = dbGet("SELECT COUNT(*) AS count FROM entities");
    const relCount = dbGet("SELECT COUNT(*) AS count FROM relationships");
    const sessionCount = dbGet(
      "SELECT COUNT(*) AS count FROM extraction_queue WHERE status = 'completed'"
    );
    const totalSessions = dbGet("SELECT COUNT(*) AS count FROM extraction_queue");
    const topEntities = dbAll(
      "SELECT name, entity_type, mention_count FROM entities ORDER BY mention_count DESC LIMIT 10"
    );
    const typeBreakdown = dbAll(
      "SELECT entity_type, COUNT(*) AS count FROM entities GROUP BY entity_type ORDER BY count DESC"
    );

    // Handle async (sqlite3 fallback)
    if (entityCount && typeof entityCount.then === "function") {
      return Promise.all([
        entityCount,
        relCount,
        sessionCount,
        totalSessions,
        topEntities,
        typeBreakdown,
      ])
        .then(
          ([
            ec,
            rc,
            sc,
            ts,
            te,
            tb,
          ]) => {
            return buildStatsMarkdown(ec, rc, sc, ts, te, tb);
          }
        )
        .catch((e) => `Graph query error: ${e.message}`);
    }

    return buildStatsMarkdown(
      entityCount,
      relCount,
      sessionCount,
      totalSessions,
      topEntities,
      typeBreakdown
    );
  } catch (e) {
    return `Graph query error: ${e.message}`;
  }
}

function buildStatsMarkdown(entityCount, relCount, sessionCount, totalSessions, topEntities, typeBreakdown) {
  let md = "## Graph Memory Statistics\n\n";
  md += "| Metric | Count |\n";
  md += "|--------|-------|\n";
  md += `| Total Entities | ${entityCount?.count ?? 0} |\n`;
  md += `| Total Relationships | ${relCount?.count ?? 0} |\n`;
  md += `| Sessions Processed | ${sessionCount?.count ?? 0} |\n`;
  md += `| Total Sessions (incl. pending/failed) | ${totalSessions?.count ?? 0} |\n\n`;

  md += "### Entity Types\n\n";
  md += "| Type | Count |\n";
  md += "|------|-------|\n";
  for (const t of typeBreakdown ?? []) {
    md += `| ${t.entity_type || "uncategorized"} | ${t.count} |\n`;
  }
  md += "\n";

  md += "### Top 10 Entities by Mention Count\n\n";
  md += "| Rank | Entity | Type | Mentions |\n";
  md += "|------|--------|------|----------|\n";
  (topEntities ?? []).forEach((e, i) => {
    md += `| ${i + 1} | ${e.name} | ${e.entity_type} | ${e.mention_count} |\n`;
  });

  return md.trim();
}

/* ── graph_related ───────────────────────────── */

/**
 * Traverse relationships from an entity.
 * @param {string} entity
 * @param {number} [depth=2]
 * @returns {string} markdown
 */
function graph_related(entity, depth = 2) {
  const health = checkHealth();
  if (!health.ok) return health.error;

  const name = typeof entity === "string" ? entity.trim() : "";
  if (!name) return "Graph query error: entity must be a non-empty string";

  const maxDepth = Math.min(Math.max(1, Number(depth) || 2), 5);

  try {
    if (queryBridge) {
      // Verify entity exists
      const exists = queryBridge.lookup(name);
      if (!exists) {
        return `Entity '${entity}' not found in graph memory.`;
      }

      const results = queryBridge.traverse(name, maxDepth);
      if (results.length === 0) {
        return `## Entities Related to "${name}"\n\nNo relationships found for this entity in graph memory.`;
      }
      return buildRelatedMarkdown(name, maxDepth, results);
    }

    // Fallback: direct SQL traversal (BFS)
    const startRow = dbGet(
      "SELECT * FROM entities WHERE name = ? COLLATE NOCASE OR canonical_name = ? COLLATE NOCASE LIMIT 1",
      [name, name]
    );

    if (startRow && typeof startRow.then === "function") {
      return startRow
        .then((row) => {
          if (!row) return `Entity '${entity}' not found in graph memory.`;
          return bfsFallback(name, maxDepth);
        })
        .catch((e) => `Graph query error: ${e.message}`);
    }

    if (!startRow) {
      return `Entity '${entity}' not found in graph memory.`;
    }

    return bfsFallback(name, maxDepth);
  } catch (e) {
    return `Graph query error: ${e.message}`;
  }
}

function buildRelatedMarkdown(name, maxDepth, results) {
  let md = `## Entities Related to "${name}"\n`;
  md += `**Traversal depth:** ${maxDepth} | **Related entities found:** ${results.length}\n\n`;
  md += "---\n\n";

  // Group by path length
  const byDepth = {};
  for (const r of results) {
    const d = r.path.length;
    if (!byDepth[d]) byDepth[d] = [];
    byDepth[d].push(r);
  }

  for (let d = 1; d <= maxDepth; d++) {
    const group = byDepth[d] || [];
    if (group.length === 0) continue;

    md += `### ${d} hop${d > 1 ? "s" : ""} away\n\n`;
    for (const r of group) {
      const pathStr = r.path
        .map((p) => `${p.name} [${p.relation ?? "related"}]`)
        .join(" → ");
      md += `- ${pathStr}\n`;
      if (r.entity) {
        const ent = r.entity;
        md += `  - Type: ${ent.type ?? "unknown"}`;
        if (ent.mentions) md += ` | Mentions: ${ent.mentions}`;
        if (ent.description) md += ` | ${ent.description}`;
        md += "\n";
      }
    }
    md += "\n";
  }

  return md.trim();
}

/** BFS traversal using direct SQL (fallback when bridge unavailable) */
function bfsFallback(startName, maxDepth) {
  const visited = new Set([startName.toLowerCase()]);
  const results = [];
  let current = [{ name: startName, path: [] }];

  for (let d = 0; d < maxDepth; d++) {
    const next = [];
    for (const node of current) {
      // Outgoing + incoming in one query
      const sql =
        "SELECT target AS name, relation_type FROM relationships WHERE source = ? COLLATE NOCASE " +
        "UNION ALL " +
        "SELECT source AS name, relation_type FROM relationships WHERE target = ? COLLATE NOCASE";
      const rows = dbAll(sql, [node.name, node.name]);

      // Handle async
      if (rows && typeof rows.then === "function") {
        return rows.then((resolved) => {
          for (const n of resolved) {
            if (!visited.has(n.name.toLowerCase())) {
              visited.add(n.name.toLowerCase());
              const newPath = [
                ...node.path,
                { name: n.name, relation: n.relation_type },
              ];
              results.push({ path: newPath, entity: null });
              next.push({ name: n.name, path: newPath });
            }
          }
          current = next;
        });
      }

      for (const n of rows) {
        if (!visited.has(n.name.toLowerCase())) {
          visited.add(n.name.toLowerCase());
          const newPath = [
            ...node.path,
            { name: n.name, relation: n.relation_type },
          ];
          results.push({ path: newPath, entity: null });
          next.push({ name: n.name, path: newPath });
        }
      }
    }
    current = next;
    if (current.length === 0) break;
  }

  if (results.length === 0) {
    return `## Entities Related to "${startName}"\n\nNo relationships found for this entity in graph memory.`;
  }
  return buildRelatedMarkdown(startName, maxDepth, results);
}

/* ── Exports ─────────────────────────────────── */
module.exports = {
  graph_search,
  graph_stats,
  graph_related,
};
