import path from 'path';
import fs from 'fs';
import initSqlJs, { Database as SqlJsDatabase } from 'sql.js';

let _SQL: any = null;

function getBaseDir(): string {
    return process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/root', '.openclaw');
}

function getDbPath(): string {
    return path.join(getBaseDir(), 'memory', 'main.sqlite');
}

function getScoresPath(): string {
    return path.join(getBaseDir(), 'memory', 'utility_scores.json');
}

async function getSqlJs() {
    if (!_SQL) _SQL = await initSqlJs();
    return _SQL;
}

// ── Read-only access to OpenClaw's main.sqlite ──────────────────────────

/** Open a read-only snapshot. Caller must close(). */
async function openDb(): Promise<SqlJsDatabase | null> {
    const SQL = await getSqlJs();
    const dbPath = getDbPath();
    if (!fs.existsSync(dbPath)) return null;
    const buffer = fs.readFileSync(dbPath);
    return new SQL.Database(buffer);
}

function queryAll(db: SqlJsDatabase, sql: string, params?: any[]): any[] {
    const stmt = db.prepare(sql);
    if (params) stmt.bind(params);
    const rows: any[] = [];
    while (stmt.step()) {
        rows.push(stmt.getAsObject());
    }
    stmt.free();
    return rows;
}

// ── Plugin-owned utility scores (JSON sidecar) ─────────────────────────

type ScoreMap = Record<string, number>;

function loadScores(): ScoreMap {
    const p = getScoresPath();
    if (!fs.existsSync(p)) return {};
    try {
        return JSON.parse(fs.readFileSync(p, 'utf8'));
    } catch {
        return {};
    }
}

function saveScores(scores: ScoreMap): void {
    const p = getScoresPath();
    const dir = path.dirname(p);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(p, JSON.stringify(scores, null, 2));
}

/** Get utility score for a memory ID (default 0.5). */
export function getUtilityScore(id: string): number {
    const scores = loadScores();
    return scores[id] !== undefined ? scores[id] : 0.5;
}

// ── FTS5 Pre-filter + Dedup ─────────────────────────────────────────────

/** Fast BM25 pre-filter via FTS5. Falls back to keyword matching if FTS5 unavailable. */
export async function searchChunksFTS(query: string, limit: number = 20): Promise<any[]> {
    const db = await openDb();
    if (!db) return [];

    try {
        const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table' OR type='virtual'");
        const hasFTS = tables.some((t: any) => t.name === 'chunks_fts');

        let rows: any[];
        if (hasFTS) {
            // FTS5 MATCH — sanitize query for FTS syntax (wrap tokens in quotes)
            const sanitized = query.replace(/[^\w\s]/g, '').split(/\s+/).filter(Boolean).map(t => `"${t}"`).join(' OR ');
            if (!sanitized) { db.close(); return []; }
            try {
                rows = queryAll(db, `SELECT chunks_fts.id, chunks_fts.text, chunks_fts.path, chunks_fts.source, rank
                    FROM chunks_fts
                    WHERE chunks_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?`, [sanitized, limit]);
            } catch {
                // FTS5 might not be compiled into sql.js — fall back
                rows = [];
            }
        } else {
            rows = [];
        }

        // Fallback: keyword pre-filter in JS if FTS5 unavailable or returned nothing
        if (rows.length === 0) {
            const allChunks = queryAll(db, `SELECT * FROM chunks ORDER BY rowid DESC LIMIT 200`);
            const queryTokens = new Set(query.toLowerCase().split(/\W+/).filter(t => t.length > 2));
            rows = allChunks.filter((row: any) => {
                const text = (row.text || '').toLowerCase();
                let matches = 0;
                for (const token of queryTokens) {
                    if (text.includes(token)) matches++;
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
    } catch (e: any) {
        db.close();
        console.error('[openclaw-memory-max][db] FTS search failed:', e.message);
        return [];
    }
}

/** Check for duplicate content. Returns chunks with high text overlap. */
export async function findSimilarChunks(text: string, limit: number = 5): Promise<any[]> {
    // Use FTS5 with the first ~50 words of the text as query
    const queryText = text.split(/\s+/).slice(0, 50).join(' ');
    return searchChunksFTS(queryText, limit);
}

// ── Public API ──────────────────────────────────────────────────────────

/** One-time schema check — read-only, no writes to main.sqlite. */
export async function ensureUtilityColumn() {
    const db = await openDb();
    if (!db) {
        console.log('[openclaw-memory-max][db] DB file not found. Awaiting context instantiation.');
        return;
    }

    try {
        const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table'");
        console.log('[openclaw-memory-max][db] Auditing tables:', tables.map((t: any) => t.name).join(', '));

        const hasChunks = tables.some((t: any) => t.name === 'chunks');
        if (hasChunks) {
            console.log('[openclaw-memory-max][db] Memory table found. Utility scores stored in sidecar file.');
        } else {
            console.log('[openclaw-memory-max][db] Memory table not found. Awaiting context instantiation.');
        }

        db.close();
    } catch (e: any) {
        db.close();
        console.error('[openclaw-memory-max][db] SQLite Audit Failed:', e.message);
    }
}

/** Update utility score in the sidecar file. Validates the ID exists in main.sqlite first. */
export async function rewardMemory(id: string, scalar: number = 0.1): Promise<boolean> {
    try {
        // Verify the memory ID actually exists in main.sqlite
        const db = await openDb();
        if (!db) return false;

        let found = false;
        try {
            const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table'");
            const targets = ['chunks', 'memories', 'documents', 'episodic_memory'];
            for (const tbl of targets) {
                if (!tables.some((t: any) => t.name === tbl)) continue;
                const rows = queryAll(db, `SELECT 1 FROM ${tbl} WHERE id = ? LIMIT 1`, [id]);
                if (rows.length > 0) { found = true; break; }
            }
        } finally {
            db.close();
        }

        if (!found) return false;

        const scores = loadScores();
        const current = scores[id] !== undefined ? scores[id] : 0.5;
        const updated = Math.max(0.0, Math.min(1.0, current + scalar));
        scores[id] = updated;
        saveScores(scores);
        console.log(`[openclaw-memory-max][db] Updated utility for ${id}: ${current.toFixed(2)} → ${updated.toFixed(2)}`);
        return true;
    } catch (e: any) {
        console.error('[openclaw-memory-max][db] Failed to update utility score:', e.message);
        return false;
    }
}

/** Query chunks table — read-only from main.sqlite, enriched with sidecar scores. */
export async function queryChunks(limit: number = 100): Promise<any[]> {
    const db = await openDb();
    if (!db) return [];

    try {
        const tables = queryAll(db, "SELECT name FROM sqlite_master WHERE type='table'");
        const hasChunks = tables.some((t: any) => t.name === 'chunks');
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
    } catch (e: any) {
        db.close();
        console.error('[openclaw-memory-max][db] Failed to query chunks:', e.message);
        return [];
    }
}
