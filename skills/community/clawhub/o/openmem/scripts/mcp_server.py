#!/usr/bin/env python3
"""
OpenMem - MCP Server
Exposes memory operations as structured tool calls via the Model Context Protocol.

Registered in OpenClaw via:
  openclaw mcp set openmem '{"command":"python3","args":["<path>/mcp_server.py"]}'

Tools exposed:
  memory_search  - Full-text search memories
  memory_add     - Add or update a memory
  memory_update  - Update content/category/importance of an existing memory
  memory_delete  - Delete a memory by ID
  memory_list    - List recent memories
  memory_stats   - Database statistics

Transport: MCP stdio (newline-delimited JSON-RPC 2.0)
"""

import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_DB = Path(
    os.environ.get("OPENMEM_DB", "~/.openclaw/workspace/memory/openmem.db")
).expanduser()

CATEGORIES = ("fact", "insight", "preference", "correction", "event", "general")
SERVER_NAME = "openmem"
SERVER_VERSION = "1.3.0"
CACHE_LIMIT = int(os.environ.get("OPENMEM_BOOTSTRAP_LIMIT", "20"))


def write_cache(db: sqlite3.Connection) -> None:
    """Write top memories to JSON cache for the bootstrap hook."""
    cache_path = DEFAULT_DB.parent / "openmem-cache.json"
    try:
        rows = db.execute(
            "SELECT id, content, category, importance FROM memories "
            "ORDER BY importance DESC, created_at DESC LIMIT ?",
            (CACHE_LIMIT,)
        ).fetchall()
        cache = {"updated_at": int(time.time()), "memories": [dict(r) for r in rows]}
        cache_path.write_text(json.dumps(cache, indent=2))
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Database (inline — no dep on mem.py to keep server self-contained)
# ---------------------------------------------------------------------------

def open_db() -> sqlite3.Connection:
    DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(DEFAULT_DB))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    _init_schema(db)
    return db


def _init_schema(db: sqlite3.Connection) -> None:
    db.executescript("""
        CREATE TABLE IF NOT EXISTS memories (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            content      TEXT    NOT NULL,
            category     TEXT    NOT NULL DEFAULT 'general',
            source       TEXT    NOT NULL DEFAULT 'manual',
            importance   REAL    NOT NULL DEFAULT 0.5,
            session_id   TEXT,
            created_at   INTEGER NOT NULL,
            updated_at   INTEGER NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_memories_content ON memories(content);
        CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category, created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC, created_at DESC);
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            content, content='memories', content_rowid='id', tokenize='porter ascii'
        );
        CREATE TRIGGER IF NOT EXISTS memories_fts_insert
            AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
            END;
        CREATE TRIGGER IF NOT EXISTS memories_fts_delete
            AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content)
                    VALUES ('delete', old.id, old.content);
            END;
        CREATE TRIGGER IF NOT EXISTS memories_fts_update
            AFTER UPDATE OF content ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content)
                    VALUES ('delete', old.id, old.content);
                INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
            END;
    """)
    db.commit()


def _row(row: sqlite3.Row) -> dict:
    d = dict(row)
    # Humanize timestamps for LLM readability
    for key in ("created_at", "updated_at"):
        if d.get(key):
            import datetime
            d[key + "_human"] = datetime.datetime.fromtimestamp(d[key]).strftime("%Y-%m-%d %H:%M")
    return d

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def _is_wildcard_query(query: str) -> bool:
    return "*" in query or "?" in query


def _wildcard_to_like(query: str) -> str:
    """Convert shell-style wildcards (* and ?) to SQL LIKE pattern."""
    pattern = query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pattern = pattern.replace("*", "%").replace("?", "_")
    return pattern


def tool_memory_search(db, args: dict) -> dict:
    query = (args.get("query") or "").strip()
    if not query:
        return {"error": "query is required"}

    limit = min(int(args.get("limit", 10)), 50)
    category = args.get("category")

    if _is_wildcard_query(query):
        # LIKE search — no relevance ranking, sort by importance + recency
        like_pattern = _wildcard_to_like(query)
        sql = """
            SELECT id, content, category, source, importance,
                   created_at, updated_at, access_count
            FROM memories
            WHERE content LIKE ? ESCAPE '\\' COLLATE NOCASE
        """
        params = [like_pattern]

        if category:
            sql += " AND category = ?"
            params.append(category)

        sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)
    else:
        # FTS search ranked by relevance + importance + recency
        sql = """
            SELECT m.id, m.content, m.category, m.source, m.importance,
                   m.created_at, m.updated_at, m.access_count,
                   bm25(memories_fts) AS fts_rank
            FROM memories_fts
            JOIN memories m ON memories_fts.rowid = m.id
            WHERE memories_fts MATCH ?
        """
        params = [query]

        if category:
            sql += " AND m.category = ?"
            params.append(category)

        sql += """
            ORDER BY (bm25(memories_fts) - m.importance * 2.0
                      - (CAST(strftime('%s','now') AS REAL) - m.created_at) / 86400.0 * 0.05)
            LIMIT ?
        """
        params.append(limit)

    rows = db.execute(sql, params).fetchall()

    for row in rows:
        db.execute("UPDATE memories SET access_count = access_count + 1 WHERE id = ?", (row["id"],))
    if rows:
        db.commit()

    return {
        "count": len(rows),
        "memories": [_row(r) for r in rows],
    }


def _significant_words(text: str) -> set:
    """Extract meaningful words for duplicate detection."""
    stopwords = {"the", "that", "this", "with", "from", "have", "will", "been",
                 "they", "were", "when", "what", "which", "there", "their",
                 "them", "then", "than", "your", "also", "into", "some",
                 "just", "over", "like", "such", "only", "more", "very"}
    words = set(re.findall(r"\b[a-zA-Z]{4,}\b", text.lower()))
    return words - stopwords


def _find_similar(db, content: str, threshold: float = 0.65) -> Optional[dict]:
    """Return existing memory if word-overlap with content exceeds threshold."""
    words = _significant_words(content)
    if len(words) < 3:
        return None
    query_words = list(words)[:6]
    fts_query = " OR ".join(f'"{w}"' for w in query_words)
    try:
        rows = db.execute(
            "SELECT m.id, m.content, m.importance FROM memories m "
            "JOIN memories_fts ON m.id = memories_fts.rowid "
            "WHERE memories_fts MATCH ? LIMIT 10",
            (fts_query,)
        ).fetchall()
    except Exception:
        return None
    for row in rows:
        existing_words = _significant_words(row["content"])
        if not existing_words:
            continue
        overlap = len(words & existing_words) / min(len(words), len(existing_words))
        if overlap >= threshold:
            return dict(row)
    return None


def tool_memory_add(db, args: dict) -> dict:
    content = (args.get("content") or "").strip()
    if not content:
        return {"error": "content is required"}

    category = args.get("category", "general")
    if category not in CATEGORIES:
        return {"error": f"category must be one of: {', '.join(CATEGORIES)}"}

    importance = float(args.get("importance", 0.5))
    importance = max(0.0, min(1.0, importance))
    source = str(args.get("source", "agent"))
    session_id = args.get("session_id")
    now = int(time.time())

    # Semantic duplicate check (unless caller opts out)
    if args.get("check_duplicate", True):
        similar = _find_similar(db, content)
        if similar:
            # Bump importance if new value is higher
            if importance > similar["importance"]:
                db.execute("UPDATE memories SET importance = ?, updated_at = ? WHERE id = ?",
                           (importance, now, similar["id"]))
                db.commit()
                write_cache(db)
                return {"added": False, "updated": True, "id": similar["id"],
                        "note": "similar memory exists — importance raised",
                        "existing": similar["content"][:120]}
            return {"added": False, "updated": False, "id": similar["id"],
                    "note": "similar memory already exists",
                    "existing": similar["content"][:120]}

    try:
        cur = db.execute(
            """INSERT INTO memories (content, category, source, importance, session_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (content, category, source, importance, session_id, now, now)
        )
        db.commit()
        write_cache(db)
        return {"added": True, "id": cur.lastrowid, "category": category, "importance": importance}
    except sqlite3.IntegrityError:
        # Exact duplicate on content column
        row = db.execute("SELECT id, importance FROM memories WHERE content = ?", (content,)).fetchone()
        if row and importance > row["importance"]:
            db.execute("UPDATE memories SET importance = ?, updated_at = ? WHERE id = ?",
                       (importance, now, row["id"]))
            db.commit()
            write_cache(db)
            return {"added": False, "updated": True, "id": row["id"],
                    "note": "exact duplicate — importance raised"}
        return {"added": False, "updated": False, "id": row["id"] if row else None,
                "note": "exact duplicate — no change needed"}


def tool_memory_update(db, args: dict) -> dict:
    mem_id = args.get("id")
    if not mem_id:
        return {"error": "id is required"}

    row = db.execute("SELECT * FROM memories WHERE id = ?", (int(mem_id),)).fetchone()
    if not row:
        return {"error": f"memory #{mem_id} not found"}

    now = int(time.time())
    fields, params = ["updated_at = ?"], [now]

    if "content" in args:
        content = args["content"].strip()
        if not content:
            return {"error": "content cannot be empty"}
        fields.append("content = ?")
        params.append(content)

    if "category" in args:
        if args["category"] not in CATEGORIES:
            return {"error": f"category must be one of: {', '.join(CATEGORIES)}"}
        fields.append("category = ?")
        params.append(args["category"])

    if "importance" in args:
        imp = max(0.0, min(1.0, float(args["importance"])))
        fields.append("importance = ?")
        params.append(imp)

    if len(fields) == 1:
        return {"error": "no fields to update (provide content, category, or importance)"}

    params.append(int(mem_id))
    db.execute(f"UPDATE memories SET {', '.join(fields)} WHERE id = ?", params)
    db.commit()
    write_cache(db)

    updated = db.execute("SELECT * FROM memories WHERE id = ?", (int(mem_id),)).fetchone()
    return {"updated": True, "memory": _row(updated)}


def tool_memory_delete(db, args: dict) -> dict:
    mem_id = args.get("id")
    if not mem_id:
        return {"error": "id is required"}

    cur = db.execute("DELETE FROM memories WHERE id = ?", (int(mem_id),))
    db.commit()
    write_cache(db)

    if cur.rowcount == 0:
        return {"error": f"memory #{mem_id} not found"}
    return {"deleted": True, "id": int(mem_id)}


def tool_memory_list(db, args: dict) -> dict:
    limit = min(int(args.get("limit", 10)), 100)
    category = args.get("category")
    order = args.get("order", "importance")  # importance | recent | access

    order_clause = {
        "importance": "importance DESC, created_at DESC",
        "recent": "created_at DESC",
        "access": "access_count DESC, importance DESC",
    }.get(order, "importance DESC, created_at DESC")

    sql = "SELECT * FROM memories"
    params = []

    if category:
        sql += " WHERE category = ?"
        params.append(category)

    sql += f" ORDER BY {order_clause} LIMIT ?"
    params.append(limit)

    rows = db.execute(sql, params).fetchall()
    return {
        "count": len(rows),
        "memories": [_row(r) for r in rows],
    }


def tool_memory_stats(db, _args: dict) -> dict:
    total = db.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    by_cat = db.execute(
        "SELECT category, COUNT(*) AS count, AVG(importance) AS avg_importance, "
        "MAX(created_at) AS latest "
        "FROM memories GROUP BY category ORDER BY count DESC"
    ).fetchall()
    oldest = db.execute("SELECT MIN(created_at) FROM memories").fetchone()[0]
    newest = db.execute("SELECT MAX(created_at) FROM memories").fetchone()[0]

    import datetime
    return {
        "total_memories": total,
        "by_category": [dict(r) for r in by_cat],
        "oldest_memory": datetime.datetime.fromtimestamp(oldest).strftime("%Y-%m-%d") if oldest else None,
        "newest_memory": datetime.datetime.fromtimestamp(newest).strftime("%Y-%m-%d") if newest else None,
        "db_path": str(DEFAULT_DB),
    }


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOLS = {
    "memory_search": {
        "description": "Search long-term memories using full-text search. Returns memories ranked by relevance, importance, and recency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query. Supports FTS5 syntax: phrases in quotes, AND/OR/NOT operators, prefix* wildcards."
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default: 10, max: 50)",
                    "default": 10
                },
                "category": {
                    "type": "string",
                    "enum": list(CATEGORIES),
                    "description": "Filter by category (optional)"
                }
            },
            "required": ["query"]
        },
        "fn": tool_memory_search,
    },
    "memory_add": {
        "description": "Add a new long-term memory. Automatically checks for similar existing memories (word-overlap deduplication) — returns the existing memory ID if a near-duplicate is found instead of inserting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The memory text. Be specific and self-contained — this will be read without conversation context."
                },
                "category": {
                    "type": "string",
                    "enum": list(CATEGORIES),
                    "description": "fact=objective info | insight=learned pattern | preference=user desire | correction=mistake+fix | event=something that happened | general=other",
                    "default": "general"
                },
                "importance": {
                    "type": "number",
                    "description": "0.0-1.0. 0.9+=critical, 0.7-0.8=important, 0.5=normal, 0.3=low",
                    "default": 0.5,
                    "minimum": 0.0,
                    "maximum": 1.0
                },
                "source": {
                    "type": "string",
                    "description": "Where this came from (e.g. 'agent', 'session:uuid', 'user')",
                    "default": "agent"
                },
                "check_duplicate": {
                    "type": "boolean",
                    "description": "Check for semantically similar memories before inserting (default: true). Set false to force insert.",
                    "default": True
                }
            },
            "required": ["content"]
        },
        "fn": tool_memory_add,
    },
    "memory_update": {
        "description": "Update an existing memory's content, category, or importance by ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Memory ID (from search or list results)"
                },
                "content": {
                    "type": "string",
                    "description": "New content (optional)"
                },
                "category": {
                    "type": "string",
                    "enum": list(CATEGORIES),
                    "description": "New category (optional)"
                },
                "importance": {
                    "type": "number",
                    "description": "New importance 0.0-1.0 (optional)",
                    "minimum": 0.0,
                    "maximum": 1.0
                }
            },
            "required": ["id"]
        },
        "fn": tool_memory_update,
    },
    "memory_delete": {
        "description": "Permanently delete a memory by ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Memory ID to delete"
                }
            },
            "required": ["id"]
        },
        "fn": tool_memory_delete,
    },
    "memory_list": {
        "description": "List memories sorted by importance, recency, or access count.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max results (default: 10, max: 100)",
                    "default": 10
                },
                "category": {
                    "type": "string",
                    "enum": list(CATEGORIES),
                    "description": "Filter by category (optional)"
                },
                "order": {
                    "type": "string",
                    "enum": ["importance", "recent", "access"],
                    "description": "Sort order: importance (default), recent, access",
                    "default": "importance"
                }
            },
        },
        "fn": tool_memory_list,
    },
    "memory_stats": {
        "description": "Get statistics about the memory database: total count, breakdown by category, date range.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
        "fn": tool_memory_stats,
    },
}

# ---------------------------------------------------------------------------
# MCP stdio transport (newline-delimited JSON-RPC 2.0)
# ---------------------------------------------------------------------------

def read_message():
    """Read one newline-delimited JSON-RPC message from stdin.

    Returns the parsed message dict, or None on EOF. Blank lines and
    unparseable lines are skipped so a single bad line does not kill
    the server.
    """
    while True:
        line = sys.stdin.readline()
        if not line:
            return None  # EOF
        line = line.strip()
        if not line:
            continue  # blank line — skip
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue  # malformed line — skip


def write_message(obj: dict) -> None:
    """Write one newline-delimited JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def make_response(req_id, result) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def make_error(req_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


# ---------------------------------------------------------------------------
# Request handlers
# ---------------------------------------------------------------------------

def handle_initialize(req_id, _params) -> dict:
    return make_response(req_id, {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    })


def handle_tools_list(req_id, _params) -> dict:
    tools = []
    for name, defn in TOOLS.items():
        tools.append({
            "name": name,
            "description": defn["description"],
            "inputSchema": defn["inputSchema"],
        })
    return make_response(req_id, {"tools": tools})


def handle_tools_call(req_id, params, db) -> dict:
    name = params.get("name", "")
    args = params.get("arguments", {})

    if name not in TOOLS:
        return make_error(req_id, -32601, f"Unknown tool: {name}")

    try:
        result = TOOLS[name]["fn"](db, args)
    except Exception as e:
        return make_error(req_id, -32603, f"Tool error: {e}")

    # MCP tool result format
    return make_response(req_id, {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, indent=2, default=str),
            }
        ],
        "isError": "error" in result,
    })


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    db = open_db()

    while True:
        msg = read_message()
        if msg is None:
            break

        req_id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params", {})

        if method == "initialize":
            write_message(handle_initialize(req_id, params))
        elif method == "initialized":
            pass  # notification, no response
        elif method == "tools/list":
            write_message(handle_tools_list(req_id, params))
        elif method == "tools/call":
            write_message(handle_tools_call(req_id, params, db))
        elif method == "ping":
            write_message(make_response(req_id, {}))
        elif req_id is not None:
            # Unknown method with an ID — must respond
            write_message(make_error(req_id, -32601, f"Method not found: {method}"))
        # Notifications (no id) are silently ignored

    db.close()


if __name__ == "__main__":
    main()
