"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getUtilityScore = getUtilityScore;
exports.searchChunksFTS = searchChunksFTS;
exports.findSimilarChunks = findSimilarChunks;
exports.ensureUtilityColumn = ensureUtilityColumn;
exports.rewardMemory = rewardMemory;
exports.queryChunks = queryChunks;
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const sql_js_1 = __importDefault(require("sql.js"));
let _SQL = null;
function getBaseDir() {
    return process.env.OPENCLAW_HOME || path_1.default.join(process.env.HOME || '/root', '.openclaw');
}
function getDbPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'main.sqlite');
}
function getScoresPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'utility_scores.json');
}
async function getSqlJs() {
    if (!_SQL)
        _SQL = await (0, sql_js_1.default)();
    return _SQL;
}
// ── Read-only access to OpenClaw's main.sqlite ──────────────────────────
/** Open a read-only snapshot. Caller must close(). */
async function openDb() {
    const SQL = await getSqlJs();
    const dbPath = getDbPath();
    if (!fs_1.default.existsSync(dbPath))
        return null;
    const buffer = fs_1.default.readFileSync(dbPath);
    return new SQL.Database(buffer);
}
function queryAll(db, sql, params) {
    const stmt = db.prepare(sql);
    if (params)
        stmt.bind(params);
    const rows = [];
    while (stmt.step()) {
        rows.push(stmt.getAsObject());
    }
    stmt.free();
    return rows;
}
function loadScores() {
    const p = getScoresPath();
    if (!fs_1.default.existsSync(p))
        return {};
    try {
        return JSON.parse(fs_1.default.readFileSync(p, 'utf8'));
    }
    catch {
        return {};
    }
}
function saveScores(scores) {
    const p = getScoresPath();
    const dir = path_1.default.dirname(p);
    if (!fs_1.default.existsSync(dir))
        fs_1.default.mkdirSync(dir, { recursive: true });
    fs_1.default.writeFileSync(p, JSON.stringify(scores, null, 2));
}
/** Get utility score for a memory ID (default 0.5). */
function getUtilityScore(id) {
    const scores = loadScores();
    return scores[id] !== undefined ? scores[id] : 0.5;
}
// ── FTS5 Pre-filter + Dedup ─────────────────────────────────────────────
/** Fast BM25 pre-filter via FTS5. Falls back to keyword matching if FTS5 unavailable. */
async function searchChunksFTS(query, limit = 20) {
    const db = await openDb();
    if (!db)
        return [];
    try {
        const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table' OR type='virtual'");
        const hasFTS = tables.some((t) => t.name === 'chunks_fts');
        let rows;
        if (hasFTS) {
            // FTS5 MATCH — sanitize query for FTS syntax (wrap tokens in quotes)
            const sanitized = query.replace(/[^\w\s]/g, '').split(/\s+/).filter(Boolean).map(t => `"${t}"`).join(' OR ');
            if (!sanitized) {
                db.close();
                return [];
            }
            try {
                rows = queryAll(db, `SELECT chunks_fts.id, chunks_fts.text, chunks_fts.path, chunks_fts.source, rank
                    FROM chunks_fts
                    WHERE chunks_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?`, [sanitized, limit]);
            }
            catch {
                // FTS5 might not be compiled into sql.js — fall back
                rows = [];
            }
        }
        else {
            rows = [];
        }
        // Fallback: keyword pre-filter in JS if FTS5 unavailable or returned nothing
        if (rows.length === 0) {
            const allChunks = queryAll(db, `SELECT * FROM chunks ORDER BY rowid DESC LIMIT 200`);
            const queryTokens = new Set(query.toLowerCase().split(/\W+/).filter(t => t.length > 2));
            rows = allChunks.filter((row) => {
                const text = (row.text || '').toLowerCase();
                let matches = 0;
                for (const token of queryTokens) {
                    if (text.includes(token))
                        matches++;
                }
                return matches >= Math.min(2, queryTokens.size);
            }).slice(0, limit);
        }
        db.close();
        // Enrich with utility scores
        const scores = loadScores();
        for (const row of rows) {
            const id = row.id || row.rowid || '';
            row.utility_score = scores[id] !== undefined ? scores[id] : 0.5;
        }
        return rows;
    }
    catch (e) {
        db.close();
        console.error('[openclaw-memory-max][db] FTS search failed:', e.message);
        return [];
    }
}
/** Check for duplicate content. Returns chunks with high text overlap. */
async function findSimilarChunks(text, limit = 5) {
    // Use FTS5 with the first ~50 words of the text as query
    const queryText = text.split(/\s+/).slice(0, 50).join(' ');
    return searchChunksFTS(queryText, limit);
}
// ── Public API ──────────────────────────────────────────────────────────
/** One-time schema check — read-only, no writes to main.sqlite. */
async function ensureUtilityColumn() {
    const db = await openDb();
    if (!db) {
        console.log('[openclaw-memory-max][db] DB file not found. Awaiting context instantiation.');
        return;
    }
    try {
        const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table'");
        console.log('[openclaw-memory-max][db] Auditing tables:', tables.map((t) => t.name).join(', '));
        const hasChunks = tables.some((t) => t.name === 'chunks');
        if (hasChunks) {
            console.log('[openclaw-memory-max][db] Memory table found. Utility scores stored in sidecar file.');
        }
        else {
            console.log('[openclaw-memory-max][db] Memory table not found. Awaiting context instantiation.');
        }
        db.close();
    }
    catch (e) {
        db.close();
        console.error('[openclaw-memory-max][db] SQLite Audit Failed:', e.message);
    }
}
/** Update utility score in the sidecar file. Validates the ID exists in main.sqlite first. */
async function rewardMemory(id, scalar = 0.1) {
    try {
        // Verify the memory ID actually exists in main.sqlite
        const db = await openDb();
        if (!db)
            return false;
        let found = false;
        try {
            const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table'");
            const targets = ['chunks', 'memories', 'documents', 'episodic_memory'];
            for (const tbl of targets) {
                if (!tables.some((t) => t.name === tbl))
                    continue;
                const rows = queryAll(db, `SELECT 1 FROM ${tbl} WHERE id = ? LIMIT 1`, [id]);
                if (rows.length > 0) {
                    found = true;
                    break;
                }
            }
        }
        finally {
            db.close();
        }
        if (!found)
            return false;
        const scores = loadScores();
        const current = scores[id] !== undefined ? scores[id] : 0.5;
        const updated = Math.max(0.0, Math.min(1.0, current + scalar));
        scores[id] = updated;
        saveScores(scores);
        console.log(`[openclaw-memory-max][db] Updated utility for ${id}: ${current.toFixed(2)} → ${updated.toFixed(2)}`);
        return true;
    }
    catch (e) {
        console.error('[openclaw-memory-max][db] Failed to update utility score:', e.message);
        return false;
    }
}
/** Query chunks table — read-only from main.sqlite, enriched with sidecar scores. */
async function queryChunks(limit = 100) {
    const db = await openDb();
    if (!db)
        return [];
    try {
        const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table'");
        const hasChunks = tables.some((t) => t.name === 'chunks');
        if (!hasChunks) {
            db.close();
            return [];
        }
        const rows = queryAll(db, `SELECT * FROM chunks ORDER BY rowid DESC LIMIT ?`, [limit]);
        db.close();
        // Enrich with sidecar utility scores
        const scores = loadScores();
        for (const row of rows) {
            const id = row.id || row.rowid || '';
            row.utility_score = scores[id] !== undefined ? scores[id] : 0.5;
        }
        return rows;
    }
    catch (e) {
        db.close();
        console.error('[openclaw-memory-max][db] Failed to query chunks:', e.message);
        return [];
    }
}
