"""
Nex Life Logger - SQLite storage layer
CC BY-NC 4.0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import sqlite3
import platform
import datetime as dt
import math
from pathlib import Path
from contextlib import contextmanager
from config import DB_PATH, DATA_DIR


def init_db():
    """Create database and tables if they don't exist. Sets secure file permissions."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if platform.system() != "Windows":
        os.chmod(str(DATA_DIR), stat.S_IRWXU)
    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS activities (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT    NOT NULL,
                source      TEXT    NOT NULL,
                kind        TEXT    NOT NULL,
                title       TEXT,
                url         TEXT,
                extra       TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_activities_ts
                ON activities(timestamp);
            CREATE INDEX IF NOT EXISTS idx_activities_kind
                ON activities(kind);
            CREATE INDEX IF NOT EXISTS idx_activities_source
                ON activities(source);

            CREATE TABLE IF NOT EXISTS summaries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                period      TEXT    NOT NULL,
                start_date  TEXT    NOT NULL,
                end_date    TEXT    NOT NULL,
                content     TEXT    NOT NULL,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_summaries_unique
                ON summaries(period, start_date);

            CREATE TABLE IF NOT EXISTS sync_state (
                source          TEXT PRIMARY KEY,
                last_timestamp  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS keywords (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword     TEXT    NOT NULL,
                category    TEXT,
                source_type TEXT    NOT NULL,
                source_date TEXT    NOT NULL,
                frequency   INTEGER DEFAULT 1,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_keywords_word
                ON keywords(keyword);
            CREATE INDEX IF NOT EXISTS idx_keywords_date
                ON keywords(source_date);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_keywords_unique
                ON keywords(keyword, source_type, source_date);

            CREATE TABLE IF NOT EXISTS transcripts (
                video_id    TEXT PRIMARY KEY,
                title       TEXT,
                transcript  TEXT NOT NULL,
                created_at  TEXT DEFAULT (datetime('now'))
            );
        """)
        conn.execute("PRAGMA journal_mode=WAL")
        _init_fts(conn)


def _init_fts(conn):
    """Create FTS5 virtual tables for full-text search if they don't exist."""
    # FTS5 index for activities (title + url)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_activities USING fts5(
            title, url, content='activities', content_rowid='id',
            tokenize='porter unicode61'
        )
    """)
    # FTS5 index for transcripts (title + transcript)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_transcripts USING fts5(
            title, transcript, content='transcripts',
            content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    # FTS5 index for summaries (content)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_summaries USING fts5(
            content, content='summaries', content_rowid='id',
            tokenize='porter unicode61'
        )
    """)
    # Triggers to keep FTS in sync with source tables
    conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS fts_activities_ai AFTER INSERT ON activities BEGIN
            INSERT INTO fts_activities(rowid, title, url)
            VALUES (new.id, new.title, new.url);
        END;
        CREATE TRIGGER IF NOT EXISTS fts_activities_ad AFTER DELETE ON activities BEGIN
            INSERT INTO fts_activities(fts_activities, rowid, title, url)
            VALUES ('delete', old.id, old.title, old.url);
        END;
        CREATE TRIGGER IF NOT EXISTS fts_activities_au AFTER UPDATE ON activities BEGIN
            INSERT INTO fts_activities(fts_activities, rowid, title, url)
            VALUES ('delete', old.id, old.title, old.url);
            INSERT INTO fts_activities(rowid, title, url)
            VALUES (new.id, new.title, new.url);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_transcripts_ai AFTER INSERT ON transcripts BEGIN
            INSERT INTO fts_transcripts(rowid, title, transcript)
            VALUES (new.rowid, new.title, new.transcript);
        END;
        CREATE TRIGGER IF NOT EXISTS fts_transcripts_ad AFTER DELETE ON transcripts BEGIN
            INSERT INTO fts_transcripts(fts_transcripts, rowid, title, transcript)
            VALUES ('delete', old.rowid, old.title, old.transcript);
        END;

        CREATE TRIGGER IF NOT EXISTS fts_summaries_ai AFTER INSERT ON summaries BEGIN
            INSERT INTO fts_summaries(rowid, content)
            VALUES (new.id, new.content);
        END;
        CREATE TRIGGER IF NOT EXISTS fts_summaries_ad AFTER DELETE ON summaries BEGIN
            INSERT INTO fts_summaries(fts_summaries, rowid, content)
            VALUES ('delete', old.id, old.content);
        END;
    """)


def rebuild_fts():
    """Rebuild all FTS indexes from scratch. Call after bulk imports or DB sync."""
    with _connect() as conn:
        _init_fts(conn)
        conn.execute("INSERT INTO fts_activities(fts_activities) VALUES ('rebuild')")
        conn.execute("INSERT INTO fts_transcripts(fts_transcripts) VALUES ('rebuild')")
        conn.execute("INSERT INTO fts_summaries(fts_summaries) VALUES ('rebuild')")


@contextmanager
def _connect():
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_activities(rows):
    if not rows:
        return
    with _connect() as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO activities (timestamp, source, kind, title, url, extra)
               VALUES (:timestamp, :source, :kind, :title, :url, :extra)""",
            rows,
        )


def get_activities(start, end):
    with _connect() as conn:
        cur = conn.execute(
            "SELECT * FROM activities WHERE timestamp >= ? AND timestamp < ? ORDER BY timestamp",
            (start, end),
        )
        return [dict(r) for r in cur.fetchall()]


def get_sync_ts(source):
    with _connect() as conn:
        row = conn.execute(
            "SELECT last_timestamp FROM sync_state WHERE source = ?", (source,)
        ).fetchone()
        return row["last_timestamp"] if row else None


def set_sync_ts(source, ts):
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO sync_state (source, last_timestamp) VALUES (?, ?)",
            (source, ts),
        )


def save_summary(period, start_date, end_date, content):
    with _connect() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO summaries (period, start_date, end_date, content)
               VALUES (?, ?, ?, ?)""",
            (period, start_date, end_date, content),
        )


def get_summary(period, start_date):
    with _connect() as conn:
        row = conn.execute(
            "SELECT content FROM summaries WHERE period = ? AND start_date = ?",
            (period, start_date),
        ).fetchone()
        return row["content"] if row else None


def get_summaries_in_range(period, start, end):
    with _connect() as conn:
        cur = conn.execute(
            """SELECT * FROM summaries
               WHERE period = ? AND start_date >= ? AND start_date < ?
               ORDER BY start_date""",
            (period, start, end),
        )
        return [dict(r) for r in cur.fetchall()]


def save_keywords(keywords):
    if not keywords:
        return
    with _connect() as conn:
        for kw in keywords:
            conn.execute(
                """INSERT INTO keywords (keyword, category, source_type, source_date, frequency)
                   VALUES (:keyword, :category, :source_type, :source_date, 1)
                   ON CONFLICT(keyword, source_type, source_date)
                   DO UPDATE SET frequency = frequency + 1""",
                kw,
            )


def get_keywords_for_date(date):
    with _connect() as conn:
        cur = conn.execute(
            "SELECT keyword, category, frequency FROM keywords WHERE source_date = ? ORDER BY frequency DESC",
            (date,),
        )
        return [dict(r) for r in cur.fetchall()]


def get_top_keywords(limit=50):
    with _connect() as conn:
        cur = conn.execute(
            """SELECT keyword, category, SUM(frequency) as total_freq,
                      COUNT(DISTINCT source_date) as days_seen
               FROM keywords
               GROUP BY keyword
               ORDER BY total_freq DESC
               LIMIT ?""",
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]


def get_keywords_for_period(start, end):
    with _connect() as conn:
        cur = conn.execute(
            """SELECT keyword, category, SUM(frequency) as total_freq,
                      COUNT(DISTINCT source_date) as days_seen
               FROM keywords
               WHERE source_date >= ? AND source_date < ?
               GROUP BY keyword
               ORDER BY total_freq DESC
               LIMIT 100""",
            (start, end),
        )
        return [dict(r) for r in cur.fetchall()]


def save_transcript(video_id, transcript, title=""):
    with _connect() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO transcripts (video_id, title, transcript)
               VALUES (?, ?, ?)""",
            (video_id, title, transcript),
        )


def get_transcript(video_id):
    with _connect() as conn:
        row = conn.execute(
            "SELECT transcript FROM transcripts WHERE video_id = ?", (video_id,)
        ).fetchone()
        return row["transcript"] if row else None


def get_transcripts_for_period(start, end):
    with _connect() as conn:
        cur = conn.execute(
            """SELECT t.video_id, t.title, t.transcript, a.timestamp
               FROM transcripts t
               JOIN activities a ON json_extract(a.extra, '$.video_id') = t.video_id
               WHERE a.kind = 'youtube' AND a.timestamp >= ? AND a.timestamp < ?
               ORDER BY a.timestamp""",
            (start, end),
        )
        return [dict(r) for r in cur.fetchall()]


# ── FTS5 Search ──────────────────────────────────

def _recency_score(timestamp_str):
    """Calculate a recency weight: newer = higher score. Returns 0.0-1.0."""
    try:
        ts = dt.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        now = dt.datetime.now(dt.timezone.utc)
        age_days = max((now - ts).total_seconds() / 86400, 0.001)
        return 1.0 / (1.0 + math.log1p(age_days))
    except Exception:
        return 0.1


def fts_search_activities(query, kind=None, source=None, since=None, until=None, limit=30):
    """Full-text search across activities with optional filters and relevance ranking."""
    with _connect() as conn:
        # Build FTS query - use simple terms for porter stemming
        fts_terms = query.strip()

        sql = """
            SELECT a.id, a.timestamp, a.source, a.kind, a.title, a.url, a.extra,
                   fts_activities.rank as fts_rank
            FROM fts_activities
            JOIN activities a ON a.id = fts_activities.rowid
            WHERE fts_activities MATCH ?
        """
        params = [fts_terms]

        if kind:
            sql += " AND a.kind = ?"
            params.append(kind)
        if source:
            sql += " AND a.source = ?"
            params.append(source)
        if since:
            sql += " AND a.timestamp >= ?"
            params.append(since)
        if until:
            sql += " AND a.timestamp < ?"
            params.append(until)

        sql += " ORDER BY fts_activities.rank LIMIT ?"
        params.append(limit)

        try:
            rows = conn.execute(sql, params).fetchall()
            results = []
            for r in rows:
                d = dict(r)
                recency = _recency_score(d["timestamp"])
                # FTS5 rank is negative (closer to 0 = worse). Normalize to 0-1 range
                # and combine with recency for final relevance score
                fts_score = min(abs(d["fts_rank"]) * 1e6, 1.0)
                d["relevance"] = round(fts_score * 0.6 + recency * 0.4, 4)
                results.append(d)
            results.sort(key=lambda x: x["relevance"], reverse=True)
            return results
        except sqlite3.OperationalError:
            # FTS table not populated yet, fall back to LIKE
            return _fallback_search_activities(query, kind, source, since, until, limit)


def fts_search_transcripts(query, since=None, until=None, limit=10):
    """Full-text search across YouTube transcripts."""
    with _connect() as conn:
        fts_terms = query.strip()

        sql = """
            SELECT t.video_id, t.title, SUBSTR(t.transcript, 1, 300) as snippet,
                   fts_transcripts.rank as fts_rank
            FROM fts_transcripts
            JOIN transcripts t ON t.rowid = fts_transcripts.rowid
            WHERE fts_transcripts MATCH ?
        """
        params = [fts_terms]

        if since or until:
            sql = """
                SELECT t.video_id, t.title, SUBSTR(t.transcript, 1, 300) as snippet,
                       fts_transcripts.rank as fts_rank, a.timestamp
                FROM fts_transcripts
                JOIN transcripts t ON t.rowid = fts_transcripts.rowid
                LEFT JOIN activities a ON json_extract(a.extra, '$.video_id') = t.video_id
                    AND a.kind = 'youtube'
                WHERE fts_transcripts MATCH ?
            """
            if since:
                sql += " AND (a.timestamp >= ? OR a.timestamp IS NULL)"
                params.append(since)
            if until:
                sql += " AND (a.timestamp < ? OR a.timestamp IS NULL)"
                params.append(until)

        sql += " ORDER BY fts_transcripts.rank LIMIT ?"
        params.append(limit)

        try:
            return [dict(r) for r in conn.execute(sql, params).fetchall()]
        except sqlite3.OperationalError:
            return _fallback_search_transcripts(query, limit)


def fts_search_summaries(query, since=None, until=None, limit=10):
    """Full-text search across AI summaries."""
    with _connect() as conn:
        fts_terms = query.strip()

        sql = """
            SELECT s.id, s.period, s.start_date, s.end_date,
                   SUBSTR(s.content, 1, 300) as snippet,
                   fts_summaries.rank as fts_rank
            FROM fts_summaries
            JOIN summaries s ON s.id = fts_summaries.rowid
            WHERE fts_summaries MATCH ?
        """
        params = [fts_terms]

        if since:
            sql += " AND s.start_date >= ?"
            params.append(since[:10])
        if until:
            sql += " AND s.start_date < ?"
            params.append(until[:10])

        sql += " ORDER BY fts_summaries.rank LIMIT ?"
        params.append(limit)

        try:
            return [dict(r) for r in conn.execute(sql, params).fetchall()]
        except sqlite3.OperationalError:
            return _fallback_search_summaries(query, limit)


def fts_search_keywords(query, category=None, limit=15):
    """Search keywords using LIKE (keywords are short, FTS5 is overkill here)."""
    with _connect() as conn:
        words = query.split()
        clauses = " OR ".join("keyword LIKE ?" for _ in words)
        params = ["%%%s%%" % w for w in words]

        sql = "SELECT keyword, category, SUM(frequency) as freq FROM keywords WHERE (%s)" % clauses
        if category:
            sql += " AND category = ?"
            params.append(category)
        sql += " GROUP BY keyword ORDER BY freq DESC LIMIT ?"
        params.append(limit)

        return [dict(r) for r in conn.execute(sql, params).fetchall()]


# ── Fallback LIKE search (when FTS not populated) ──

def _fallback_search_activities(query, kind=None, source=None, since=None, until=None, limit=30):
    with _connect() as conn:
        words = query.split()
        like_clauses = " AND ".join("(title LIKE ? OR url LIKE ?)" for _ in words)
        params = []
        for w in words:
            params.extend(["%%%s%%" % w, "%%%s%%" % w])

        sql = "SELECT id, timestamp, source, kind, title, url, extra FROM activities WHERE %s" % like_clauses
        if kind:
            sql += " AND kind = ?"
            params.append(kind)
        if source:
            sql += " AND source = ?"
            params.append(source)
        if since:
            sql += " AND timestamp >= ?"
            params.append(since)
        if until:
            sql += " AND timestamp < ?"
            params.append(until)
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        results = []
        for r in rows:
            d = dict(r)
            d["fts_rank"] = 0
            d["relevance"] = _recency_score(d["timestamp"])
            results.append(d)
        return results


def _fallback_search_transcripts(query, limit=10):
    with _connect() as conn:
        words = query.split()
        clauses = " OR ".join("(title LIKE ? OR transcript LIKE ?)" for _ in words)
        params = []
        for w in words:
            params.extend(["%%%s%%" % w, "%%%s%%" % w])
        sql = "SELECT video_id, title, SUBSTR(transcript, 1, 300) as snippet FROM transcripts WHERE %s LIMIT ?" % clauses
        params.append(limit)
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def _fallback_search_summaries(query, limit=10):
    with _connect() as conn:
        words = query.split()
        clauses = " OR ".join("content LIKE ?" for _ in words)
        params = ["%%%s%%" % w for w in words]
        sql = "SELECT id, period, start_date, end_date, SUBSTR(content, 1, 300) as snippet FROM summaries WHERE (%s) ORDER BY start_date DESC LIMIT ?" % clauses
        params.append(limit)
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
