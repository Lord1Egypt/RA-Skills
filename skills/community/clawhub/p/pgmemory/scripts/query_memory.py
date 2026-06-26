#!/usr/bin/env python3
"""
pgmemory query_memory.py — search and inspect memories

Usage:
  python3 query_memory.py "database connection"          # semantic search
  python3 query_memory.py --importance 3 --limit 20      # load critical memories
  python3 query_memory.py --category decision             # filter by category
  python3 query_memory.py --stats                         # show counts and health
  python3 query_memory.py --list                          # list all memory keys
  python3 query_memory.py --include-archived "search"    # search archive too
  python3 query_memory.py --restore "key.name"           # restore archived memory
  python3 query_memory.py --harvest <subagent-namespace> # harvest sub-agent memories
  python3 query_memory.py --check                        # connectivity check only (exit 0=ok, 1=warn, 2=down)
"""

import argparse, json, os, sys
from pathlib import Path

SKILL_DIR      = Path(__file__).parent.parent
DEFAULT_CONFIG = Path.home() / ".openclaw" / "pgmemory.json"

def load_config(path: Path) -> dict:
    if not path.exists():
        print(f"Config not found: {path}\nRun: python3 {SKILL_DIR}/scripts/setup.py", file=sys.stderr)
        sys.exit(1)
    with open(path) as f: return json.load(f)

def get_embed(text: str, config: dict):
    provider = config.get("embeddings", {}).get("provider", "voyage")
    key_env  = config.get("embeddings", {}).get("api_key_env", "VOYAGE_API_KEY")
    # Prefer api_key stored directly in config; fall back to env var
    api_key  = config.get("embeddings", {}).get("api_key") or os.environ.get(key_env, "")
    model    = config.get("embeddings", {}).get("model")
    import urllib.request
    try:
        if provider == "voyage":
            data = json.dumps({"input": [text], "model": model or "voyage-3"}).encode()
            req  = urllib.request.Request("https://api.voyageai.com/v1/embeddings", data=data,
                       headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=15).read())["data"][0]["embedding"]
        elif provider == "openai":
            data = json.dumps({"input": text, "model": model or "text-embedding-3-small"}).encode()
            req  = urllib.request.Request("https://api.openai.com/v1/embeddings", data=data,
                       headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=15).read())["data"][0]["embedding"]
        elif provider == "ollama":
            data = json.dumps({"model": model or "nomic-embed-text", "prompt": text}).encode()
            req  = urllib.request.Request("http://localhost:11434/api/embeddings", data=data,
                       headers={"Content-Type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=15).read())["embedding"]
    except Exception as e:
        print(f"Embedding failed: {e}", file=sys.stderr)
        return None

def fmt_row(row, show_score=True) -> str:
    key, category, importance, content, relevance, updated_at = row[:6]
    stars = "★" * importance + "☆" * (3 - importance)
    score = f"  rel={relevance:.2f}" if show_score else ""
    date  = str(updated_at)[:10] if updated_at else "?"
    short = content[:120] + ("…" if len(content) > 120 else "")
    return f"[{category}/{stars}]{score}  {key}  ({date})\n    {short}"

def main():
    p = argparse.ArgumentParser(description="Search and inspect pgmemory memories")
    p.add_argument("query",           nargs="?",  help="Semantic search query")
    p.add_argument("--agent",         default=None, help="Agent namespace (default: from config)")
    p.add_argument("--importance",    type=int,   choices=[1,2,3], help="Filter by minimum importance level")
    p.add_argument("--category",      default=None, choices=["decision","constraint","infrastructure","vision","preference","context","task","all"], help="Filter by category")
    p.add_argument("--limit",         type=int,   default=10, help="Max results to return (default: 10)")
    p.add_argument("--stats",         action="store_true", help="Show memory counts and health stats")
    p.add_argument("--list",          action="store_true", help="List all memory keys")
    p.add_argument("--include-archived", action="store_true", help="Also search archived memories")
    p.add_argument("--restore",       metavar="KEY", help="Restore archived memory by key")
    p.add_argument("--harvest",       metavar="NAMESPACE", help="Harvest memories from a sub-agent namespace")
    p.add_argument("--harvest-threshold", type=int, default=2, metavar="N", help="Only harvest memories with importance >= N (default: 2)")
    p.add_argument("--config",        default=str(DEFAULT_CONFIG), help=f"Path to pgmemory.json (default: {DEFAULT_CONFIG})")
    p.add_argument("--json",          action="store_true", help="Output results as JSON")
    p.add_argument("--check",         action="store_true", help="Connectivity check only — exit 0=ok, 2=unreachable")
    args = p.parse_args()

    config     = load_config(Path(args.config))
    agent_name = args.agent or config.get("agent", {}).get("name", "main")

    try:
        import psycopg2
        db_uri = config.get("db", {}).get("uri", "")
        # Add connect_timeout if not already in URI
        uri_with_timeout = db_uri + ("&" if "?" in db_uri else "?") + "connect_timeout=5"
        conn = psycopg2.connect(uri_with_timeout)
        conn.autocommit = True
        cur  = conn.cursor()
    except Exception as e:
        host = db_uri.split("@")[-1].split("/")[0] if "@" in db_uri else db_uri
        print(f"\n⚠️  pgmemory UNREACHABLE — {host}", file=sys.stderr)
        print(f"   Error: {e}", file=sys.stderr)
        print(f"   Falling back to MEMORY.md and daily memory files.", file=sys.stderr)
        print(f"   Fix: check DB at {host} and verify pgmemory.json config.", file=sys.stderr)
        sys.exit(2)

    if args.check:
        try:
            cur.execute("SELECT COUNT(*) FROM memories")
            count = cur.fetchone()[0]
            print(f"✓ pgmemory OK — {count:,} memories accessible")
            sys.exit(0)
        except Exception as e:
            print(f"\n⚠️  pgmemory connected but schema missing: {e}", file=sys.stderr)
            print(f"   Run: python3 {SKILL_DIR}/scripts/setup.py --migrate", file=sys.stderr)
            sys.exit(2)

    # ── Stats ──────────────────────────────────────────────────────────────────
    if args.stats:
        cur.execute("SELECT COUNT(*) FROM memories WHERE agent=%s", (agent_name,))
        active = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM archived_memories WHERE agent=%s", (agent_name,))
        archived = cur.fetchone()[0]
        cur.execute("""
            SELECT category, COUNT(*), AVG(relevance_score)::numeric(4,2)
            FROM memories WHERE agent=%s GROUP BY category ORDER BY COUNT(*) DESC
        """, (agent_name,))
        by_cat = cur.fetchall()
        cur.execute("""
            SELECT importance, COUNT(*) FROM memories
            WHERE agent=%s GROUP BY importance ORDER BY importance DESC
        """, (agent_name,))
        by_imp = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM memories WHERE agent=%s AND embedding IS NULL", (agent_name,))
        no_embed = cur.fetchone()[0]

        if args.json:
            print(json.dumps({"agent": agent_name, "active": active, "archived": archived,
                               "by_category": {r[0]: {"count": r[1], "avg_relevance": float(r[2])} for r in by_cat},
                               "by_importance": {r[0]: r[1] for r in by_imp},
                               "missing_embeddings": no_embed}))
        else:
            print(f"\npgmemory stats — agent: {agent_name}")
            print(f"  Active:   {active:,}  |  Archived: {archived:,}  |  No embedding: {no_embed}")
            print(f"\n  By category:")
            for cat, count, avg_rel in by_cat:
                print(f"    {cat:<20} {count:>5}  avg_relevance={avg_rel}")
            print(f"\n  By importance:")
            for imp, count in by_imp:
                stars = "★" * imp + "☆" * (3-imp)
                print(f"    {stars}  {count:>5}")
        cur.close(); conn.close(); return

    # ── List ───────────────────────────────────────────────────────────────────
    if args.list:
        q    = "SELECT key, category, importance, updated_at FROM memories WHERE agent=%s"
        vals = [agent_name]
        if args.category and args.category != 'all':   q += " AND category=%s"; vals.append(args.category)
        if args.importance: q += " AND importance=%s"; vals.append(args.importance)
        q += " ORDER BY importance DESC, category, key"
        cur.execute(q, vals)
        rows = cur.fetchall()
        if args.json:
            print(json.dumps([{"key":r[0],"category":r[1],"importance":r[2],"updated":str(r[3])} for r in rows]))
        else:
            for key, cat, imp, upd in rows:
                print(f"  {'★'*imp+'☆'*(3-imp)}  [{cat}]  {key}  ({str(upd)[:10]})")
        cur.close(); conn.close(); return

    # ── Restore ────────────────────────────────────────────────────────────────
    if args.restore:
        cur.execute("""
            SELECT agent,key,category,content,importance,source,tags,expires_at
            FROM archived_memories WHERE agent=%s AND key=%s ORDER BY archived_at DESC LIMIT 1
        """, (agent_name, args.restore))
        row = cur.fetchone()
        if not row:
            print(f"No archived memory found: {args.restore}"); cur.close(); conn.close(); return
        conn.autocommit = False
        cur.execute("""
            INSERT INTO memories (agent,key,category,content,importance,source,tags,expires_at,relevance_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1.0)
            ON CONFLICT (agent,key) DO UPDATE SET
                content=EXCLUDED.content, relevance_score=1.0, updated_at=NOW()
        """, row)
        cur.execute("DELETE FROM archived_memories WHERE agent=%s AND key=%s", (agent_name, args.restore))
        conn.commit()
        print(f"✓ Restored: {args.restore}")
        cur.close(); conn.close(); return

    # ── Harvest ────────────────────────────────────────────────────────────────
    if args.harvest:
        src_ns = args.harvest
        cur.execute("""
            SELECT key, category, content, importance, embedding
            FROM memories WHERE agent=%s AND importance>=%s AND key NOT LIKE '%%:summary'
        """, (src_ns, args.harvest_threshold))
        rows = cur.fetchall()
        conn.autocommit = False
        promoted = skipped = 0
        for key, category, content, importance, embedding in rows:
            # Check similarity against existing primary memories
            if embedding:
                cur.execute("""
                    SELECT 1 FROM memories
                    WHERE agent=%s AND embedding IS NOT NULL
                    AND 1-(embedding<=>%s::vector) > 0.95 LIMIT 1
                """, (agent_name, embedding))
                if cur.fetchone(): skipped += 1; continue

            new_key = f"from:{src_ns}:{key}"
            if embedding:
                cur.execute("""
                    INSERT INTO memories (agent,key,category,content,embedding,importance,source)
                    VALUES (%s,%s,%s,%s,%s::vector,%s,%s)
                    ON CONFLICT (agent,key) DO UPDATE SET
                        content=EXCLUDED.content, importance=EXCLUDED.importance, updated_at=NOW()
                """, (agent_name, new_key, category, content, embedding, importance, f"harvest:{src_ns}"))
            else:
                cur.execute("""
                    INSERT INTO memories (agent,key,category,content,importance,source)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (agent,key) DO NOTHING
                """, (agent_name, new_key, category, content, importance, f"harvest:{src_ns}"))
            promoted += 1

        conn.commit()
        print(f"✓ Harvested from {src_ns}: {promoted} promoted, {skipped} skipped (duplicate)")
        cur.close(); conn.close(); return

    # ── Semantic search ────────────────────────────────────────────────────────
    results = []

    if args.query:
        vec = get_embed(args.query, config)
        if not vec:
            print("Embedding failed — cannot run semantic search", file=sys.stderr); sys.exit(1)

        emb_str = f"[{','.join(str(x) for x in vec)}]"

        # Build filter
        filters = ["agent=%s", "embedding IS NOT NULL"]
        vals    = [agent_name]
        if args.importance: filters.append("importance>=%s"); vals.append(args.importance)
        if args.category and args.category != 'all':   filters.append("category=%s");   vals.append(args.category)
        where = " AND ".join(filters)

        cur.execute(f"""
            SELECT key, category, importance, content, relevance_score, updated_at,
                   1-(embedding<=>%s::vector) AS similarity
            FROM memories WHERE {where}
            ORDER BY embedding<=>%s::vector
            LIMIT %s
        """, [emb_str] + vals + [emb_str, args.limit])
        results = [(*r[:6], r[6]) for r in cur.fetchall()]

        # Auto-update access_count + last_accessed
        if results:
            keys = [r[0] for r in results]
            cur.execute("""
                UPDATE memories SET access_count=access_count+1, last_accessed=NOW()
                WHERE agent=%s AND key=ANY(%s)
            """, (agent_name, keys))

        # Optionally search archive too
        if args.include_archived:
            cur.execute(f"""
                SELECT key, category, importance, content, 0.0, archived_at,
                       1-(embedding<=>%s::vector) AS similarity
                FROM archived_memories WHERE agent=%s
                AND embedding IS NOT NULL AND 1-(embedding<=>%s::vector) > 0.5
                ORDER BY similarity DESC LIMIT 5
            """, [emb_str, agent_name, emb_str])
            archive_rows = cur.fetchall()
            if archive_rows:
                print(f"\n{len(archive_rows)} archived result(s):")
                for r in archive_rows:
                    print(f"  [ARCHIVED] {fmt_row(r)}")
                    info_restore = f"  Restore: python3 {SKILL_DIR}/scripts/query_memory.py --restore \"{r[0]}\""
                    print(info_restore)

    else:
        # No query — load by importance/category
        filters = ["agent=%s"]
        vals    = [agent_name]
        if args.importance: filters.append("importance>=%s"); vals.append(args.importance)
        if args.category and args.category != 'all':   filters.append("category=%s");   vals.append(args.category)
        where = " AND ".join(filters)

        cur.execute(f"""
            SELECT key, category, importance, content, relevance_score, updated_at, relevance_score
            FROM memories WHERE {where}
            ORDER BY importance DESC, relevance_score DESC
            LIMIT %s
        """, vals + [args.limit])
        results = list(cur.fetchall())

    cur.close(); conn.close()

    if not results:
        print("No memories found.")
        return

    if args.json:
        out = [{"key":r[0],"category":r[1],"importance":r[2],"content":r[3],
                "relevance":float(r[4] or 0),"updated":str(r[5]),"similarity":float(r[6] or 0)}
               for r in results]
        print(json.dumps(out, indent=2))
    else:
        query_label = f'"{args.query}"' if args.query else f"importance>={args.importance or 1}"
        print(f"\n{len(results)} result(s) for {query_label} — agent: {agent_name}\n")
        for r in results:
            print(fmt_row(r))
            if len(r) > 6 and r[6]: print(f"    similarity: {r[6]:.3f}")
            print()

if __name__ == "__main__":
    main()
