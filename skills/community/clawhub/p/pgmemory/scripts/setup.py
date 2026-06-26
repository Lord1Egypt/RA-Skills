#!/usr/bin/env python3
"""
pgmemory setup.py
─────────────────
Usage:
  python3 setup.py                  # interactive wizard
  python3 setup.py --validate       # validate config only
  python3 setup.py --migrate        # run pending migrations
  python3 setup.py --rollback 2     # rollback to schema version 2
  python3 setup.py --doctor         # full system health check
  python3 setup.py --decay          # recalculate relevance scores
  python3 setup.py --yes            # non-interactive (use defaults)
  python3 setup.py --config <path>  # use specific config file
"""

import argparse, hashlib, json, math, os, platform, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SKILL_DIR      = Path(__file__).parent.parent
MIGRATIONS_DIR = SKILL_DIR / "scripts" / "migrations"
DEFAULT_CONFIG = Path.home() / ".openclaw" / "pgmemory.json"

# ── Colours ────────────────────────────────────────────────────────────────────
USE_COLOR = sys.stdout.isatty()
def _c(code, t): return f"\033[{code}m{t}\033[0m" if USE_COLOR else t
green  = lambda t: _c("32", t)
yellow = lambda t: _c("33", t)
red    = lambda t: _c("31", t)
bold   = lambda t: _c("1",  t)
dim    = lambda t: _c("2",  t)
def ok(m):   print(f"  {green('✓')} {m}")
def warn(m): print(f"  {yellow('⚠')} {m}")
def err(m):  print(f"  {red('✗')} {m}")
def info(m): print(f"  {dim('→')} {m}")
def hdr(m):  print(f"\n{bold(m)}")

# ── Defaults ───────────────────────────────────────────────────────────────────
SANE_DEFAULTS = {
    "memory": {
        "importance_threshold_write": 2,
        "importance_threshold_load":  3,
        "save_interval_messages":     20,
        "save_interval_minutes":      30,
        "interval_write_mode":        "replace",
        "inherit_on_spawn":           True,
        "ttl_days":                   {"1": 30, "2": 180, "3": None},
        "never_expire_categories":    ["decision","constraint","infrastructure","vision","preference"],
        "dedup_window_minutes":       5,
        "similarity_dedup_threshold": 0.95,
        "max_memories":               10000,
    },
    "decay": {
        "enabled": True,
        "rates": {
            "decision": 0.001, "constraint": 0.001,
            "infrastructure": 0.003, "vision": 0.003, "preference": 0.003,
            "context": 0.05, "task": 0.1,
        },
        "reinforcement_factor": 0.1,
        "archive_threshold":    0.1,
        "restore_on_access":    True,
    },
    "archive": {
        "enabled": True, "on_expire": True, "on_evict": True,
        "on_decay": True, "archived_ttl_days": None, "restore_on_access": True,
    },
    "agents":    {"namespace_from_agent_id": True, "search_scope": "completed"},
    "subagents": {"auto_inject_context": True, "context_top_k": 5,
                  "auto_harvest_on_complete": True, "harvest_importance_threshold": 2},
}

EXPECTED_DIMS   = {"voyage": 1024, "openai": 1536, "ollama": 768}
VALID_PROVIDERS = list(EXPECTED_DIMS.keys())
VALID_CATS      = ["decision","constraint","infrastructure","vision","preference","context","task"]

# ── Config helpers ─────────────────────────────────────────────────────────────
def load_config(path: Path) -> dict:
    if not path.exists(): return {}
    with open(path) as f: return json.load(f)

def save_config(config: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(config, f, indent=2)
    print(f"\n{green('✓')} Config saved to {path}")

def merged(config: dict) -> dict:
    result = json.loads(json.dumps(SANE_DEFAULTS))
    def deep_merge(base, over):
        for k, v in over.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict): deep_merge(base[k], v)
            else: base[k] = v
    deep_merge(result, config)
    return result

# ── DB ─────────────────────────────────────────────────────────────────────────
def connect(uri: str):
    try:
        import psycopg2
        conn = psycopg2.connect(uri)
        conn.autocommit = False
        return conn
    except Exception:
        return None

def get_applied(conn) -> dict:
    cur = conn.cursor()
    try:
        cur.execute("SELECT version, checksum FROM pgmemory_migrations ORDER BY version")
        return {r[0]: r[1] for r in cur.fetchall()}
    except Exception:
        return {}
    finally:
        cur.close()

def file_md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()

def extract_section(sql: str, section: str) -> str:
    m = re.search(rf"--\s*{section}\s*\n(.*?)(?=--\s*(?:UP|DOWN)|$)", sql, re.DOTALL|re.IGNORECASE)
    return m.group(1).strip() if m else sql.strip()

def migration_files() -> list:
    result = []
    for f in sorted(MIGRATIONS_DIR.glob("*.sql")):
        m = re.match(r"^(\d+)_", f.name)
        if m: result.append((int(m.group(1)), f))
    return result

# ── Validate ───────────────────────────────────────────────────────────────────
def cmd_validate(config_path: Path) -> bool:
    hdr("Validating config")
    errors, warnings = [], []

    if not config_path.exists():
        err(f"Config not found: {config_path}")
        info("Run setup.py without flags to create one")
        return False

    try:
        config = load_config(config_path)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON: {e}"); return False
    ok("Valid JSON")

    db_uri = config.get("db", {}).get("uri", "")
    if not db_uri:                               errors.append("db.uri is required")
    elif not db_uri.startswith("postgresql"):    errors.append("db.uri must be a PostgreSQL URI")
    else:                                        ok(f"db.uri present")

    provider = config.get("embeddings", {}).get("provider", "")
    if not provider:                             errors.append("embeddings.provider is required")
    elif provider not in VALID_PROVIDERS:        errors.append(f"provider must be: {', '.join(VALID_PROVIDERS)}")
    else:                                        ok(f"embeddings.provider: {provider}")

    agent = config.get("agent", {}).get("name", "")
    if not agent: errors.append("agent.name is required")
    else:         ok(f"agent.name: {agent}")

    if provider and provider != "ollama":
        key_env     = config.get("embeddings", {}).get("api_key_env", "")
        stored_key  = config.get("embeddings", {}).get("api_key", "")
        env_key     = os.environ.get(key_env, "") if key_env else ""
        resolved    = stored_key or env_key
        if not resolved:
            if stored_key:  ok(f"embeddings.api_key stored in config")
            elif key_env:   warnings.append(f"${key_env} not set and no api_key in config")
            else:           warnings.append(f"No api_key_env or api_key configured for {provider}")
        else:
            src = "config" if stored_key else f"${key_env}"
            ok(f"API key available (from {src})")

    cfg = merged(config)
    m = cfg.get("memory", {})
    if not (1 <= m.get("importance_threshold_write", 2) <= 3):
        errors.append("importance_threshold_write must be 1-3")
    for cat, rate in cfg.get("decay", {}).get("rates", {}).items():
        if not (0.0 <= rate <= 1.0):
            errors.append(f"decay.rates.{cat}={rate} must be 0.0-1.0")
    known = {"db","embeddings","agent","memory","decay","archive","agents","subagents"}
    for k in config:
        if k not in known: warnings.append(f"Unknown config key: {k}")

    for w in warnings: warn(w)
    for e_ in errors:  err(e_)

    if errors:
        print(f"\n{red(str(len(errors)) + ' error(s)')} — fix before running setup")
        return False
    suf = f", {len(warnings)} warning(s)" if warnings else ""
    print(f"\n{green('Config is valid')}{suf}")
    return True

# ── Migrations ─────────────────────────────────────────────────────────────────
def cmd_migrate(conn) -> bool:
    hdr("Running migrations")
    cur = conn.cursor()
    # Bootstrap migrations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pgmemory_migrations (
            version INT PRIMARY KEY, filename TEXT NOT NULL,
            checksum TEXT NOT NULL, applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    conn.commit()

    applied = get_applied(conn)
    pending = 0

    for version, path in migration_files():
        checksum = file_md5(path)
        if version in applied:
            if applied[version] != checksum:
                err(f"Migration {version:04d} checksum MISMATCH — file modified after apply")
                err("Restore the original file or run --rollback before re-applying")
                return False
            continue
        try:
            cur.execute(extract_section(path.read_text(), "UP"))
            cur.execute("INSERT INTO pgmemory_migrations (version,filename,checksum) VALUES (%s,%s,%s)",
                        (version, path.name, checksum))
            conn.commit()
            ok(f"Applied {version:04d}: {path.name}")
            pending += 1
        except Exception as e:
            conn.rollback()
            err(f"Migration {version:04d} FAILED: {e}")
            return False

    cur.close()
    files = migration_files()
    latest = max(v for v,_ in files) if files else 0
    if pending == 0: ok(f"Already at version {latest:04d} — nothing to do")
    else:            ok(f"Schema now at version {latest:04d} ({pending} applied)")
    return True

def cmd_rollback(conn, target: int) -> bool:
    hdr(f"Rolling back to version {target:04d}")
    applied = get_applied(conn)
    to_rb   = sorted([(v,p) for v,p in migration_files() if v > target and v in applied],
                     key=lambda x: x[0], reverse=True)
    if not to_rb:
        ok(f"Already at or below version {target:04d}"); return True

    cur = conn.cursor()
    for version, path in to_rb:
        sql_down = extract_section(path.read_text(), "DOWN")
        if not sql_down:
            err(f"Migration {version:04d} has no DOWN section"); return False
        try:
            cur.execute(sql_down)
            cur.execute("DELETE FROM pgmemory_migrations WHERE version = %s", (version,))
            conn.commit()
            ok(f"Rolled back {version:04d}: {path.name}")
        except Exception as e:
            conn.rollback()
            err(f"Rollback {version:04d} FAILED: {e}"); return False
    cur.close()
    ok(f"Schema at version {target:04d}")
    return True

# ── Embed helpers ──────────────────────────────────────────────────────────────
def embed_text(text: str, provider: str, api_key: str, model: str = None) -> Optional[list]:
    import urllib.request
    try:
        if provider == "voyage":
            m = model or "voyage-3"
            data = json.dumps({"input": [text], "model": m}).encode()
            req  = urllib.request.Request("https://api.voyageai.com/v1/embeddings", data=data,
                       headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
            return resp["data"][0]["embedding"]
        elif provider == "openai":
            m = model or "text-embedding-3-small"
            data = json.dumps({"input": text, "model": m}).encode()
            req  = urllib.request.Request("https://api.openai.com/v1/embeddings", data=data,
                       headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
            return resp["data"][0]["embedding"]
        elif provider == "ollama":
            m = model or "nomic-embed-text"
            data = json.dumps({"model": m, "prompt": text}).encode()
            req  = urllib.request.Request("http://localhost:11434/api/embeddings", data=data,
                       headers={"Content-Type": "application/json"})
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
            return resp["embedding"]
    except Exception:
        return None

def get_stored_dims(conn) -> Optional[int]:
    cur = conn.cursor()
    try:
        cur.execute("SELECT array_length(embedding::real[], 1) FROM memories WHERE embedding IS NOT NULL LIMIT 1")
        row = cur.fetchone()
        return row[0] if row else None
    except Exception: return None
    finally: cur.close()

# ── Doctor ─────────────────────────────────────────────────────────────────────
def cmd_doctor(config: dict) -> int:
    cfg = merged(config)
    uri = config.get("db", {}).get("uri", "")
    errors, warnings = [], []

    hdr("Connectivity")
    conn = connect(uri) if uri else None
    if not conn:
        err(f"Cannot connect: {uri or '(no uri configured)'}")
        print(f"\n{red('Cannot continue — fix database connection first')}")
        return 2
    ok("Database connection OK")

    cur = conn.cursor()
    try:
        cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
        row = cur.fetchone()
        if row: ok(f"pgvector {row[0]} installed")
        else:   err("pgvector not installed"); errors.append("pgvector")
    except Exception as e:
        err(f"pgvector check failed: {e}"); errors.append("pgvector")

    cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm'")
    if cur.fetchone(): ok("pg_trgm installed")
    else: warn("pg_trgm not installed (optional)"); warnings.append("pg_trgm")

    hdr("Schema")
    applied  = get_applied(conn)
    files    = migration_files()
    if files:
        latest  = max(v for v,_ in files)
        current = max(applied.keys()) if applied else 0
        if current >= latest: ok(f"Schema at version {current:04d} (latest)")
        else:
            err(f"Schema at version {current:04d}, latest is {latest:04d}")
            info("Run: python3 setup.py --migrate"); errors.append("schema_behind")

        bad_cs = [v for v,p in files if v in applied and applied[v] != file_md5(p)]
        if bad_cs:
            for v in bad_cs: err(f"Migration {v:04d} checksum mismatch — file modified after apply")
            errors.extend([f"checksum_{v}" for v in bad_cs])
        elif applied: ok("All migration checksums verified")

    for tbl in ["memories","archived_memories","session_state","pgmemory_migrations"]:
        cur.execute("SELECT 1 FROM information_schema.tables WHERE table_name=%s", (tbl,))
        if cur.fetchone(): ok(f"Table '{tbl}' exists")
        else:
            err(f"Table '{tbl}' missing — run: python3 setup.py --migrate")
            errors.append(f"table_{tbl}")

    hdr("Embeddings")
    provider = config.get("embeddings", {}).get("provider", "")
    key_env  = config.get("embeddings", {}).get("api_key_env", "")
    api_key  = os.environ.get(key_env, "") if key_env else ""

    if not provider:
        warn("No embedding provider configured"); warnings.append("no_provider")
    else:
        if provider != "ollama" and not api_key:
            err(f"${key_env} not set"); errors.append("api_key")
        else:
            vec = embed_text("pgmemory doctor test", provider, api_key)
            if vec:
                dims = len(vec)
                ok(f"Test embed OK ({dims}-dim) via {provider}")
                stored = get_stored_dims(conn)
                if stored and stored != dims:
                    err(f"DIMENSION MISMATCH: stored={stored}, provider returns {dims}")
                    info("Option A: revert provider in pgmemory.json")
                    info("Option B: Change embeddings.provider back to the original provider")
                    info("Option C: Contact support or open an issue for --re-embed guidance")
                    errors.append("dimension_mismatch")
            else:
                err(f"Test embed FAILED — check API key / provider config")
                errors.append("embed_failed")

    hdr("Memory")
    try:
        cur.execute("SELECT COUNT(*) FROM memories")
        count = cur.fetchone()[0]
        max_m = cfg.get("memory", {}).get("max_memories", 10000)
        pct   = int(100 * count / max_m) if max_m else 0
        if max_m and pct >= 90:
            warn(f"{count:,} / {max_m:,} memories ({pct}% of cap)")
            info("Run: python3 setup.py --decay  (will archive low-relevance memories)"); warnings.append("near_cap")
        else:
            ok(f"{count:,} active memories" + (f" ({pct}% of cap)" if max_m else ""))

        cur.execute("SELECT COUNT(*) FROM memories WHERE embedding IS NULL")
        nulls = cur.fetchone()[0]
        if nulls: warn(f"{nulls:,} memories without embeddings"); warnings.append("null_embeds")
        else:     ok("All memories have embeddings")

        cur.execute("SELECT COUNT(*) FROM archived_memories")
        ok(f"{cur.fetchone()[0]:,} archived memories")
    except Exception as e:
        warn(f"Could not query memories: {e}"); warnings.append("memory_query")

    cur.close(); conn.close()
    print()
    if errors:
        print(red(f"{len(errors)} error(s), {len(warnings)} warning(s)") + " — see above")
        return 2
    elif warnings:
        print(yellow(f"0 errors, {len(warnings)} warning(s)"))
        return 1
    else:
        print(green("All checks passed ✓"))
        return 0

# ── Decay ──────────────────────────────────────────────────────────────────────
def cmd_decay(conn, config: dict) -> bool:
    hdr("Running decay cycle")
    cfg   = merged(config)
    dcfg  = cfg.get("decay", {})
    acfg  = cfg.get("archive", {})
    if not dcfg.get("enabled", True):
        info("Decay disabled in config"); return True

    rates     = dcfg.get("rates", {})
    r_factor  = dcfg.get("reinforcement_factor", 0.1)
    threshold = dcfg.get("archive_threshold", 0.1)
    on_decay  = acfg.get("on_decay", True) and acfg.get("enabled", True)

    cur = conn.cursor()
    try:
        cur.execute("SELECT id, category, importance, relevance_score, access_count, updated_at FROM memories")
        rows    = cur.fetchall()
        now     = datetime.now(timezone.utc)
        updated = archived = 0

        for mem_id, category, importance, relevance, access_count, updated_at in rows:
            if updated_at:
                if updated_at.tzinfo is None: updated_at = updated_at.replace(tzinfo=timezone.utc)
                days = (now - updated_at).total_seconds() / 86400
            else: days = 0

            base_rate  = rates.get(category, 0.05)
            imp_weight = importance / 3.0
            rate       = base_rate * (1.0 / max(imp_weight, 0.1))
            new_score  = min(1.0, math.exp(-rate * days) * (1 + math.log1p(access_count) * r_factor) * imp_weight)

            if abs(new_score - relevance) < 0.001: continue

            if new_score < threshold and on_decay:
                cur.execute("""
                    INSERT INTO archived_memories SELECT *, NOW(), 'decayed'
                    FROM memories WHERE id = %s ON CONFLICT DO NOTHING
                """, (mem_id,))
                cur.execute("DELETE FROM memories WHERE id = %s", (mem_id,))
                archived += 1
            else:
                cur.execute("UPDATE memories SET relevance_score=%s WHERE id=%s",
                            (round(new_score, 4), mem_id))
                updated += 1

        conn.commit()
        ok(f"Updated {updated:,} scores")
        if archived: ok(f"Archived {archived:,} decayed memories")
        cur.close()
        return True
    except Exception as e:
        conn.rollback(); cur.close()
        err(f"Decay failed: {e}"); return False

# ── Docker ─────────────────────────────────────────────────────────────────────
def detect_docker() -> bool:
    try:
        return subprocess.run(["docker","info"], capture_output=True, timeout=5).returncode == 0
    except Exception: return False

def install_docker(yes: bool) -> bool:
    hdr("Installing Docker")
    system = platform.system().lower()
    if system == "linux":
        if not yes and input("  Install Docker via get.docker.com? [y/n] ").lower() != "y": return False
        if subprocess.run("curl -fsSL https://get.docker.com | sh", shell=True).returncode != 0:
            err("Docker install failed"); return False
        subprocess.run(["sudo","systemctl","enable","--now","docker"], capture_output=True)
        user = os.environ.get("USER","")
        if user:
            subprocess.run(["sudo","usermod","-aG","docker",user], capture_output=True)
            warn(f"Added {user} to docker group — re-login for this to take effect")
        ok("Docker installed"); return True
    elif system == "darwin":
        if subprocess.run(["which","brew"], capture_output=True).returncode == 0:
            if not yes and input("  Install docker + colima via Homebrew? [y/n] ").lower() != "y": return False
            subprocess.run(["brew","install","docker","colima"])
            subprocess.run(["colima","start"])
            ok("Docker + Colima ready"); return True
        else:
            err("Install Docker Desktop: https://docker.com/products/docker-desktop"); return False
    err(f"Unsupported OS for auto-install: {system}"); return False

def start_postgres_docker(config_path: Path) -> Optional[str]:
    compose_path = config_path.parent / "pgmemory-compose.yml"
    compose_path.write_text("""services:
  pgmemory:
    image: pgvector/pgvector:pg17
    container_name: pgmemory
    restart: unless-stopped
    environment:
      POSTGRES_USER: openclaw
      POSTGRES_PASSWORD: pgmemory
      POSTGRES_DB: openclaw
    ports:
      - "15432:5432"
    volumes:
      - pgmemory_data:/var/lib/postgresql/data
volumes:
  pgmemory_data:
""")
    for cmd in [["docker","compose","-f",str(compose_path),"up","-d"],
                ["docker-compose","-f",str(compose_path),"up","-d"]]:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0: break
    else:
        err("Failed to start Docker container"); return None

    ok("Container started (pgvector/pgvector:pg17)")
    info("Waiting for PostgreSQL...")
    import time
    uri = "postgresql://openclaw:pgmemory@localhost:15432/openclaw"
    for _ in range(30):
        c = connect(uri)
        if c: c.close(); ok("PostgreSQL ready"); return uri
        time.sleep(1)
    err("PostgreSQL did not become ready in 30s"); return None

# ── AGENTS.md scaffold ─────────────────────────────────────────────────────────
PGMEMORY_STARTUP_MARKER = "<!-- pgmemory:startup -->"
PGMEMORY_SECTION_MARKER = "<!-- pgmemory:section -->"

def startup_steps(agent_name: str, config_path: Path) -> str:
    """The mandatory startup lines to inject into the Every Session block."""
    return f"""\
   **Query pgmemory instead of reading markdown files** — faster, focused, survives compaction. ({PGMEMORY_STARTUP_MARKER})
   ```bash
   # Check connectivity first — warns loudly if DB is down
   python3 {SKILL_DIR}/scripts/query_memory.py --check
   # Load critical memories (decisions, constraints, infrastructure)
   python3 {SKILL_DIR}/scripts/query_memory.py --importance 3 --limit 20
   # Semantic search for current task context
   python3 {SKILL_DIR}/scripts/query_memory.py "brief description of current work"
   ```
   If --check fails with exit code 2: warn the user ("⚠️ pgmemory unreachable") and fall back to MEMORY.md + daily files."""

def scaffold_agents_md(agent_name: str, db_uri: str, config_path: Path) -> str:
    """Full pgmemory reference section appended to AGENTS.md."""
    return f"""
{PGMEMORY_SECTION_MARKER}
## pgmemory — Persistent Semantic Memory

**Config:** `{config_path}`  |  **Namespace:** `{agent_name}`

pgmemory is the **default memory system**. Markdown files are the automatic backup.
Always write to both. Always read from pgmemory first.

### ⚡ Startup (MANDATORY)

```bash
# Check connectivity (warns loudly if DB is down)
python3 {SKILL_DIR}/scripts/query_memory.py --check

# Load critical memories
python3 {SKILL_DIR}/scripts/query_memory.py --importance 3 --limit 20

# Semantic search for current task context
python3 {SKILL_DIR}/scripts/query_memory.py "describe what you're working on"
```

If `--check` fails (exit 2): warn the user, fall back to reading daily markdown files.

### ✏️ Writing memories (always write to BOTH)

**1. pgmemory — primary:**
```bash
python3 {SKILL_DIR}/scripts/write_memory.py \\
  --key "unique.descriptive.key" \\
  --content "What you want to remember" \\
  --category decision \\
  --importance 3
```

**2. Daily markdown backup** — also append a brief note to `memory/YYYY-MM-DD.md`.
Full detail lives in pgmemory; markdown is the durable fallback if DB is ever unavailable.

### Categories & importance

| Category | Importance | Expires |
|---|---|---|
| decision, constraint | 3 | Never |
| infrastructure, vision, preference | 2–3 | Never or 180d |
| context | 2 | 180d |
| task | 1 | 30d |

### Maintenance

```bash
python3 {SKILL_DIR}/scripts/setup.py --doctor    # health check
python3 {SKILL_DIR}/scripts/setup.py --decay     # archive faded memories
python3 {SKILL_DIR}/scripts/query_memory.py --stats
```
"""

def inject_startup_into_agents_md(agents_md: Path, agent_name: str, config_path: Path) -> bool:
    """
    Try to inject the pgmemory startup step into the 'Every Session' numbered list.
    Returns True if injected, False if the pattern wasn't found (caller falls back to append).
    """
    content = agents_md.read_text()

    # Already injected?
    if PGMEMORY_STARTUP_MARKER in content:
        return True

    # Look for the numbered startup list — find the last "N. " item in an "Every Session" block
    # We look for a block that has "1. Read" style items and append after the last one
    import re
    # Match the last numbered item before a blank line or ## heading
    pattern = r'((?:^[ \t]*\d+\. .+\n)+)'
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    if not matches:
        return False

    # Use the last numbered list (most likely to be the startup steps)
    last_match = matches[-1]
    insert_pos = last_match.end()

    step = startup_steps(agent_name, config_path)
    new_content = content[:insert_pos] + step + "\n" + content[insert_pos:]
    agents_md.write_text(new_content)
    return True

# ── Wizard ─────────────────────────────────────────────────────────────────────
def cmd_wizard(config_path: Path, yes: bool):
    print(bold("\n╔══════════════════════════════╗"))
    print(bold("║   pgmemory setup wizard      ║"))
    print(bold("╚══════════════════════════════╝\n"))

    existing = load_config(config_path)

    # ── DB ────────────────────────────────────────────────────────────────────
    hdr("Step 1: Database")
    existing_uri = existing.get("db", {}).get("uri", "")
    if existing_uri:
        info(f"Found existing config: {config_path}")
        use_it = yes or input(f"  Use existing DB? [{existing_uri[:60]}] [Y/n] ").lower() in ("","y")
        db_uri = existing_uri if use_it else input("  Enter PostgreSQL URI: ").strip()
    else:
        print("  [1] Docker — pgvector/pgvector:pg17 (recommended)")
        print("  [2] Existing PostgreSQL")
        choice = "1" if yes else (input("  Choice [1]: ").strip() or "1")
        if choice == "1":
            if not detect_docker():
                warn("Docker not found")
                do_install = yes or input("  Install Docker? [y/n] ").lower() == "y"
                if do_install:
                    if not install_docker(yes) or not detect_docker():
                        err("Docker unavailable — install manually and retry"); sys.exit(1)
                else:
                    err("Docker required for option 1"); sys.exit(1)
            db_uri = start_postgres_docker(config_path)
            if not db_uri: sys.exit(1)
        else:
            default = "postgresql://openclaw@localhost:5432/openclaw"
            db_uri  = (input(f"  URI [{default}]: ").strip() or default) if not yes else default

    conn = connect(db_uri)
    if not conn: err(f"Cannot connect to: {db_uri}"); sys.exit(1)
    ok("Connected")

    # ── Embeddings ────────────────────────────────────────────────────────────
    hdr("Step 2: Embeddings")
    existing_provider = existing.get("embeddings", {}).get("provider", "")
    if yes:
        provider = existing_provider or "voyage"
    else:
        print("  [1] Voyage AI  — voyage-3, 1024-dim (default, best)")
        print("  [2] OpenAI     — text-embedding-3-small, 1536-dim")
        print("  [3] Ollama     — nomic-embed-text, 768-dim (local, no key)")
        choice   = input("  Choice [1]: ").strip() or "1"
        provider = {"1":"voyage","2":"openai","3":"ollama"}.get(choice, "voyage")

    key_env = api_key = ""
    if provider != "ollama":
        default_env = {"voyage":"VOYAGE_API_KEY","openai":"OPENAI_API_KEY"}.get(provider,"EMBEDDING_API_KEY")
        key_env = (input(f"  API key env var [{default_env}]: ").strip() or default_env) if not yes \
                  else existing.get("embeddings",{}).get("api_key_env", default_env)
        # Try to resolve key: existing config → env var → prompt
        stored_key = existing.get("embeddings", {}).get("api_key", "")
        api_key    = stored_key or os.environ.get(key_env, "")
        if not api_key and not yes:
            entered = input(f"  Paste {provider} API key (or leave blank to set ${key_env} later): ").strip()
            if entered: api_key = entered
        if not api_key:
            warn(f"No API key found — set ${key_env} or add api_key to config before querying")
        else:
            vec = embed_text("pgmemory setup test", provider, api_key)
            if vec: ok(f"Test embed OK ({len(vec)}-dim)")
            else:   warn("Test embed failed — check your API key")

    dims = EXPECTED_DIMS.get(provider, 1024)

    # ── Agent ─────────────────────────────────────────────────────────────────
    hdr("Step 3: Agent")
    default_agent = existing.get("agent", {}).get("name", "main")
    agent_name = default_agent if yes else (input(f"  OpenClaw agent name [{default_agent}]: ").strip() or default_agent)
    ok(f"Agent: {agent_name}")

    # ── Write config ──────────────────────────────────────────────────────────
    hdr("Step 4: Config")
    config = {"db": {"uri": db_uri},
              "embeddings": {"provider": provider, "dimensions": dims},
              "agent": {"name": agent_name}}
    if key_env: config["embeddings"]["api_key_env"] = key_env
    if api_key: config["embeddings"]["api_key"] = api_key
    for k in ("memory","decay","archive","agents","subagents"):
        if k in existing: config[k] = existing[k]
    save_config(config, config_path)

    # ── Migrate ───────────────────────────────────────────────────────────────
    hdr("Step 5: Migrations")
    if not cmd_migrate(conn): conn.close(); sys.exit(1)
    conn.close()

    # ── AGENTS.md ─────────────────────────────────────────────────────────────
    hdr("Step 6: AGENTS.md")
    workspace  = Path.home() / ".openclaw" / "workspace"
    agents_md  = workspace / "AGENTS.md"
    section    = scaffold_agents_md(agent_name, db_uri, config_path)
    if agents_md.exists():
        content = agents_md.read_text()
        if PGMEMORY_SECTION_MARKER in content:
            ok("AGENTS.md already has pgmemory section")
        elif yes or input(f"  Update {agents_md} with pgmemory? [Y/n] ").lower() in ("","y"):
            # Try to inject startup steps into the numbered list first
            injected = inject_startup_into_agents_md(agents_md, agent_name, config_path)
            if injected:
                ok("Injected startup steps into 'Every Session' list")
            else:
                warn("Could not find numbered startup list — appending section instead")
            # Always append the full reference section
            with open(agents_md, "a") as f: f.write(section)
            ok(f"pgmemory section added to {agents_md}")
    elif yes or input(f"  Create {agents_md} with pgmemory? [Y/n] ").lower() in ("","y"):
        agents_md.parent.mkdir(parents=True, exist_ok=True)
        agents_md.write_text(section)
        ok(f"Created {agents_md}")

    # ── Cron ──────────────────────────────────────────────────────────────────
    hdr("Step 7: Decay schedule")
    decay_cmd = f"0 3 * * * python3 {SKILL_DIR}/scripts/setup.py --decay --config {config_path} >> /tmp/pgmemory-decay.log 2>&1"
    if yes:
        info(f"Add cron for daily decay:\n  {decay_cmd}")
    elif input("  Add daily decay cron (3am)? [Y/n] ").lower() in ("","y"):
        try:
            existing_cron = subprocess.run(["crontab","-l"], capture_output=True, text=True).stdout
            if "pgmemory" not in existing_cron:
                proc = subprocess.run(["crontab","-"], input=existing_cron.rstrip()+"\n"+decay_cmd+"\n",
                                      text=True, capture_output=True)
                if proc.returncode == 0: ok("Cron job added")
                else: warn(f"Could not add cron: {proc.stderr}")
            else: ok("Cron already present")
        except Exception as e:
            warn(f"Could not configure cron: {e}")
            info(f"Add manually:\n  {decay_cmd}")

    print(f"\n{bold('══════════════════════════════════════')}")
    print(f"{green('pgmemory is ready!')}")
    print(f"{'══════════════════════════════════════'}")
    print(f"  Config:   {config_path}")
    print(f"  Agent:    {agent_name} ({provider}, {dims}-dim)")
    print(f"  Write:    python3 {SKILL_DIR}/scripts/write_memory.py --help")
    print(f"  Search:   python3 {SKILL_DIR}/scripts/query_memory.py --help")
    print(f"  Health:   python3 {SKILL_DIR}/scripts/setup.py --doctor\n")

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="pgmemory — persistent semantic memory for OpenClaw")
    p.add_argument("--config",   default=str(DEFAULT_CONFIG), help=f"Path to pgmemory.json (default: {DEFAULT_CONFIG})")
    p.add_argument("--validate", action="store_true", help="Validate config file and exit")
    p.add_argument("--migrate",  action="store_true", help="Run pending schema migrations")
    p.add_argument("--rollback", type=int, metavar="N", help="Roll back schema to version N")
    p.add_argument("--doctor",   action="store_true", help="Full system health check")
    p.add_argument("--decay",    action="store_true", help="Recalculate memory relevance scores and archive faded memories")
    p.add_argument("--sync-agents", action="store_true", help="Scaffold pgmemory into all OpenClaw agent workspaces")
    p.add_argument("--yes",      action="store_true", help="Non-interactive mode, accept all defaults")
    args = p.parse_args()

    config_path = Path(args.config)

    if args.validate:
        sys.exit(0 if cmd_validate(config_path) else 1)

    if args.doctor:
        sys.exit(cmd_doctor(load_config(config_path)))

    if args.migrate or args.rollback is not None:
        if not cmd_validate(config_path): sys.exit(1)
        conn = connect(load_config(config_path)["db"]["uri"])
        if not conn: err("Cannot connect"); sys.exit(1)
        ok_ = cmd_rollback(conn, args.rollback) if args.rollback is not None else cmd_migrate(conn)
        conn.close(); sys.exit(0 if ok_ else 1)

    if args.decay:
        config = load_config(config_path)
        if not config: err(f"Config not found: {config_path}"); sys.exit(1)
        conn = connect(config["db"]["uri"])
        if not conn: err("Cannot connect"); sys.exit(1)
        ok_ = cmd_decay(conn, config); conn.close(); sys.exit(0 if ok_ else 1)

    if args.sync_agents:
        config = load_config(config_path)
        if not config:
            err(f"Config not found: {config_path}"); sys.exit(1)
        ok_ = cmd_sync_agents(config_path, config['db']['uri'])
        sys.exit(0 if ok_ else 1)

    cmd_wizard(config_path, args.yes)


# ── Sync agents ────────────────────────────────────────────────────────────────
def find_openclaw_config() -> Optional[Path]:
    """Find the openclaw.json config file."""
    env_path = os.environ.get("OPENCLAW_CONFIG_PATH", "")
    candidates = [
        Path(env_path) if env_path else None,
        Path.home() / ".openclaw" / "openclaw.json",
        Path.home() / ".openclaw" / "config.json",
    ]
    for p in candidates:
        if p and p.exists() and p.is_file(): return p
    return None

def get_openclaw_agents(openclaw_config: Path) -> list:
    """Return list of {id, workspace} dicts from openclaw.json."""
    try:
        with open(openclaw_config) as f:
            data = json.load(f)
    except Exception:
        # Try JSON5-style (strip comments)
        import re
        with open(openclaw_config) as f:
            raw = f.read()
        raw = re.sub(r'//.*', '', raw)
        raw = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)
        try:
            data = json.loads(raw)
        except Exception:
            return []

    agents = []
    agent_list = data.get("agents", {}).get("list", [])
    state_dir = Path(os.environ.get("OPENCLAW_STATE_DIR", Path.home() / ".openclaw"))

    for agent in agent_list:
        agent_id = agent.get("id", "main")
        # Resolve workspace path
        workspace = agent.get("workspace")
        if workspace:
            workspace = Path(workspace.replace("~", str(Path.home())))
        else:
            workspace = state_dir / f"workspace-{agent_id}"
            if not workspace.exists() and agent_id == "main":
                workspace = state_dir / "workspace"
        agents.append({"id": agent_id, "workspace": workspace})

    # Always include main if list is empty
    if not agents:
        workspace = state_dir / "workspace"
        agents.append({"id": "main", "workspace": workspace})

    return agents

def cmd_sync_agents(config: Path, db_uri: str) -> bool:
    hdr("Syncing agents")

    oc_config = find_openclaw_config()
    if not oc_config:
        warn("Could not find openclaw.json — checking default workspace only")
        agents = [{"id": "main", "workspace": Path.home() / ".openclaw" / "workspace"}]
    else:
        info(f"Found OpenClaw config: {oc_config}")
        agents = get_openclaw_agents(oc_config)

    if not agents:
        warn("No agents found in OpenClaw config"); return True

    conn = connect(db_uri)
    if not conn:
        err(f"Cannot connect to database"); return False
    cur = conn.cursor()

    updated = 0
    for agent in agents:
        agent_id  = agent["id"]
        workspace = agent["workspace"]
        agents_md = workspace / "AGENTS.md"

        # Check if workspace exists
        if not workspace.exists():
            warn(f"{agent_id}: workspace not found ({workspace}) — skipping")
            continue

        # Check if AGENTS.md has pgmemory
        if agents_md.exists():
            content = agents_md.read_text()
            if PGMEMORY_SECTION_MARKER in content:
                ok(f"{agent_id}: already configured")
                _ensure_session_state(cur, agent_id)
                conn.commit()
                continue

        # Add pgmemory block
        section = scaffold_agents_md(agent_id, db_uri, config)
        if agents_md.exists():
            injected = inject_startup_into_agents_md(agents_md, agent_id, config)
            if injected:
                ok(f"{agent_id}: startup steps injected into 'Every Session' list")
            with open(agents_md, "a") as f: f.write(section)
        else:
            agents_md.parent.mkdir(parents=True, exist_ok=True)
            agents_md.write_text(section)

        _ensure_session_state(cur, agent_id)
        conn.commit()
        ok(f"{agent_id}: pgmemory block added → {agents_md}")
        updated += 1

    cur.close(); conn.close()
    print()
    if updated:
        ok(f"{updated} agent(s) updated, {len(agents)-updated} already configured")
    else:
        ok(f"All {len(agents)} agent(s) already have pgmemory")
    return True

def _ensure_session_state(cur, agent_id: str):
    cur.execute("""
        INSERT INTO session_state (agent) VALUES (%s)
        ON CONFLICT (agent) DO NOTHING
    """, (agent_id,))

if __name__ == "__main__":
    main()
