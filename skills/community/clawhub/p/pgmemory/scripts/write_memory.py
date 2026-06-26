#!/usr/bin/env python3
"""
pgmemory write_memory.py — write a memory to the DB

Usage:
  python3 write_memory.py --key "infra.db" --content "OVH at 10.10.0.1:5432" --importance 3 --category infrastructure
  python3 write_memory.py --key "decision.ui" --content "AI left panel ~380px" --category decision
"""

import argparse, json, os, sys
from pathlib import Path

SKILL_DIR      = Path(__file__).parent.parent
DEFAULT_CONFIG = Path.home() / ".openclaw" / "pgmemory.json"
VALID_CATS     = ["decision","constraint","infrastructure","vision","preference","context","task"]

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
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
            return resp["data"][0]["embedding"]
        elif provider == "openai":
            data = json.dumps({"input": text, "model": model or "text-embedding-3-small"}).encode()
            req  = urllib.request.Request("https://api.openai.com/v1/embeddings", data=data,
                       headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
            return resp["data"][0]["embedding"]
        elif provider == "ollama":
            data = json.dumps({"model": model or "nomic-embed-text", "prompt": text}).encode()
            req  = urllib.request.Request("http://localhost:11434/api/embeddings", data=data,
                       headers={"Content-Type": "application/json"})
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
            return resp["embedding"]
    except Exception as e:
        print(f"Embedding failed: {e}", file=sys.stderr)
        return None

def main():
    p = argparse.ArgumentParser(description="Write a memory to pgmemory")
    p.add_argument("--key",        required=True,  help="Unique key (e.g. infra.db.ovh)")
    p.add_argument("--content",    required=True,  help="Memory text")
    p.add_argument("--category",   default="context", choices=VALID_CATS)
    p.add_argument("--importance", type=int, default=2, choices=[1,2,3])
    p.add_argument("--agent",      default=None,   help="Agent name (overrides config)")
    p.add_argument("--source",     default="session")
    p.add_argument("--tags",       nargs="*",      help="Optional tags")
    p.add_argument("--config",     default=str(DEFAULT_CONFIG))
    p.add_argument("--no-embed",   action="store_true", help="Skip embedding (faster, no vector search)")
    p.add_argument("--dry-run",    action="store_true")
    args = p.parse_args()

    config     = load_config(Path(args.config))
    agent_name = args.agent or config.get("agent", {}).get("name", "main")
    cfg        = config.get("memory", {})

    # TTL calculation
    ttl_days = cfg.get("ttl_days", {}).get(str(args.importance))
    never_cats = cfg.get("never_expire_categories",
                         ["decision","constraint","infrastructure","vision","preference"])
    expires_at = None
    if args.category not in never_cats and ttl_days:
        from datetime import datetime, timezone, timedelta
        expires_at = (datetime.now(timezone.utc) + timedelta(days=ttl_days)).isoformat()

    if args.dry_run:
        print(json.dumps({
            "agent": agent_name, "key": args.key, "category": args.category,
            "importance": args.importance, "content": args.content,
            "source": args.source, "expires_at": expires_at,
        }, indent=2))
        return

    # Get embedding
    embedding = None
    if not args.no_embed:
        embedding = get_embed(args.content, config)
        if embedding is None:
            print("Warning: embedding failed — writing without vector", file=sys.stderr)

    # Connect + write
    try:
        import psycopg2
        conn = psycopg2.connect(config["db"]["uri"])
        cur  = conn.cursor()

        # Dedup check: don't rewrite same key within dedup_window_minutes
        dedup_mins = cfg.get("dedup_window_minutes", 5)
        cur.execute("""
            SELECT updated_at FROM memories
            WHERE agent=%s AND key=%s
            AND updated_at > NOW() - ((%s || ' minutes')::interval)
        """, (agent_name, args.key, dedup_mins))
        if cur.fetchone():
            print(f"Skipped (dedup window {dedup_mins}min): {args.key}")
            cur.close(); conn.close(); return

        # Upsert: update if key exists, insert if new
        if embedding:
            emb_str = f"[{','.join(str(x) for x in embedding)}]"
            cur.execute("""
                INSERT INTO memories (agent, key, category, content, embedding, importance,
                                      source, tags, expires_at)
                VALUES (%s,%s,%s,%s,%s::vector,%s,%s,%s,%s)
                ON CONFLICT (agent, key) WHERE key IS NOT NULL DO UPDATE SET
                    content=EXCLUDED.content, category=EXCLUDED.category,
                    embedding=EXCLUDED.embedding, importance=EXCLUDED.importance,
                    source=EXCLUDED.source, tags=EXCLUDED.tags,
                    expires_at=EXCLUDED.expires_at, updated_at=NOW()
            """, (agent_name, args.key, args.category, args.content, emb_str,
                  args.importance, args.source, args.tags or [], expires_at))
        else:
            cur.execute("""
                INSERT INTO memories (agent, key, category, content, importance, source, tags, expires_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (agent, key) WHERE key IS NOT NULL DO UPDATE SET
                    content=EXCLUDED.content, category=EXCLUDED.category,
                    importance=EXCLUDED.importance, source=EXCLUDED.source,
                    tags=EXCLUDED.tags, expires_at=EXCLUDED.expires_at, updated_at=NOW()
            """, (agent_name, args.key, args.category, args.content,
                  args.importance, args.source, args.tags or [], expires_at))

        conn.commit()
        cur.close(); conn.close()
        print(f"✓ Wrote [{args.category}/{args.importance}] {args.key} → {agent_name}")
        if expires_at: print(f"  Expires: {expires_at[:10]}")

    except Exception as e:
        print(f"Error writing memory: {e}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__":
    main()
