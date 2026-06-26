# Trident Deployment Guide

This guide covers three deployment tracks. **Start with Track 1** unless you already have semantic recall infrastructure.

---

## Track 1: Trident Lite (No Docker — All Platforms)

**→ For a faster, simpler setup: `references/trident-lite.md`**

Trident Lite covers the full setup for Layers 0, 0.5, and 1 with platform-specific commands for Windows, Mac, and Linux.

### Quick Summary

1. Enable `lossless-claw` plugin in `openclaw.json`
2. Create `memory/{daily,semantic,self,lessons,projects,reflections,layer0}/`
3. Copy and customize `scripts/layer0-agent-prompt-template.md` → `memory/layer0/AGENT-PROMPT.md`
4. Create Layer 0.5 cron job (every 900000ms, Haiku model, isolated session)
5. Run `template-integrity-check.sh --approve`
6. Test with `openclaw cron run --job-id <id> --run-mode force`

Full commands (including Windows PowerShell) in `references/trident-lite.md`.

---

## Track 2: Semantic Recall (Optional Upgrade)

Add vector search and entity graphs when your memory exceeds ~50K messages.

### When to Upgrade

- Layer 0.5 is missing signals because context window is too large for a 15-min window
- You want to query "what did we discuss about X six months ago?"
- You need entity relationship tracking (person → company → project → date)

### Option A: Docker Compose (Easiest)

Create `~/trident-backend/docker-compose.yml`:

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      QDRANT__SERVICE__GRPC_PORT: "6334"
    restart: unless-stopped

  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6379:6379"
    volumes:
      - falkordb_data:/data
    restart: unless-stopped

volumes:
  qdrant_data:
  falkordb_data:
```

**Start:**
```bash
cd ~/trident-backend
docker compose up -d
```

**Verify:**
```bash
curl http://localhost:6333/collections  # Qdrant: should return {"result":{"collections":[]}}
redis-cli -p 6379 ping                  # FalkorDB: should return PONG
```

---

### Option B: Native Binaries (No Docker)

**Qdrant (Linux/Mac):**
```bash
# Download latest binary
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-musl.tar.gz | tar -xz
chmod +x qdrant

# Run with persistent storage
./qdrant --storage-path ~/.qdrant-storage
```

**Qdrant (Windows PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-pc-windows-msvc.zip" -OutFile qdrant.zip
Expand-Archive qdrant.zip -DestinationPath .
.\qdrant.exe --storage-path "$env:USERPROFILE\.qdrant-storage"
```

**FalkorDB via Redis module (Linux/Mac):**
```bash
# Install Redis
apt install redis-server  # Debian/Ubuntu
# or: brew install redis  # Mac

# Download FalkorDB module
curl -L https://github.com/FalkorDB/FalkorDB/releases/latest/download/falkordb-linux-x64.so -o falkordb.so

# Start Redis with FalkorDB loaded
redis-server --loadmodule ./falkordb.so
```

---

### Option C: Cloud Services (Zero Local Infrastructure)

**Qdrant Cloud:**
1. Create free account at https://qdrant.tech (1GB cluster free)
2. Create cluster → get API key + cluster URL
3. Use in embedding script: `client = QdrantClient(url="...", api_key="...")`

**FalkorDB Cloud:**
1. Create account at https://falkordb.com
2. Free tier available
3. Get connection string: `redis://your-cluster.falkordb.io:6379`

---

### Configure Layer 0.5 for Semantic Recall

After deploying Qdrant/FalkorDB, update your `memory/layer0/AGENT-PROMPT.md` to include:

```markdown
## Pre-Turn Context Injection

Before composing any response:

1. Run Qdrant semantic search against the user's message:
   - Endpoint: http://localhost:6333 (or your cloud URL)
   - Collection: trident-memory
   - Query: embed user message, search top-5 results
   - Inject relevant chunks into context

2. Query FalkorDB for entity relationships:
   - Endpoint: localhost:6379 (Redis protocol)
   - Query: GRAPH.QUERY trident-entities "MATCH (n) WHERE n.name CONTAINS '{keyword}' RETURN n"
   - Inject relevant entity context

3. Proceed with normal signal routing.
```

**Embedding script** (Python, runs as part of Layer 0.5):
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import hashlib, json, pathlib, sys

WORKSPACE = pathlib.Path.home() / ".openclaw" / "workspace"
QDRANT_URL = "http://localhost:6333"
COLLECTION = "trident-memory"
EMBED_MODEL = "text-embedding-3-small"

openai = OpenAI()
qdrant = QdrantClient(url=QDRANT_URL)

def embed(text: str) -> list[float]:
    resp = openai.embeddings.create(input=text, model=EMBED_MODEL)
    return resp.data[0].embedding

def ensure_collection():
    existing = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION not in existing:
        qdrant.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

def index_memory_file(path: pathlib.Path):
    text = path.read_text()
    chunks = [text[i:i+500] for i in range(0, len(text), 400)]  # 100-char overlap
    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.sha256(f"{path}:{i}".encode()).hexdigest()
        point_id = int(chunk_id[:8], 16)
        qdrant.upsert(COLLECTION, points=[
            PointStruct(
                id=point_id,
                vector=embed(chunk),
                payload={"text": chunk, "source": str(path), "chunk": i}
            )
        ])

def search(query: str, top_k: int = 5):
    results = qdrant.search(COLLECTION, query_vector=embed(query), limit=top_k)
    return [r.payload["text"] for r in results]

if __name__ == "__main__":
    ensure_collection()
    for md_file in WORKSPACE.rglob("*.md"):
        if "migration-backup" not in str(md_file):
            index_memory_file(md_file)
    print(f"Indexed {len(list(WORKSPACE.rglob('*.md')))} memory files.")
```

---

## Track 3: Migration from Existing Memory

If you have an existing OpenClaw workspace with `MEMORY.md`, `SOUL.md`, or other custom files, use the migration script:

```bash
cd ~/.openclaw/skills/project-trident/scripts
chmod +x migrate-existing-memory.sh template-integrity-check.sh

# Step 1: Preview (no changes made)
./migrate-existing-memory.sh --dry-run

# Step 2: Migrate (with automatic backup)
./migrate-existing-memory.sh

# Step 3: Approve your AGENT-PROMPT.md
./template-integrity-check.sh --approve
```

### What the Script Does

1. **Backs up all existing `.md` files** to `memory/migration-backup/TIMESTAMP/`
2. **Creates Trident directory structure** (`memory/{daily,self,lessons,projects,reflections,layer0}`)
3. **Guides routing decisions interactively:**
   - `SOUL.md` → keep at root or move to `memory/self/identity.md`
   - `MEMORY.md` → stays at root, Trident header appended
   - `USER.md`, `AGENTS.md` → stay at root (no change)
   - Other `.md` files → route to semantic/self/lessons/projects/skip
4. **Installs AGENT-PROMPT.md** with your workspace path pre-filled
5. **Generates migration report** with next steps

### Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Existing memory corrupted or lost | Full backup created before any changes |
| Wrong routing decision | Dry-run preview + interactive approval |
| SOUL.md personality lost | Never moved without explicit user choice |
| Layer 0.5 breaks existing habits | Run alongside old memory for 1-2 weeks; cutover only when confident |

### Incremental Migration Strategy

For large, intricate workspaces, don't migrate everything at once:

1. **Week 1:** Install Trident Lite alongside existing memory. Let Layer 0.5 run.
2. **Week 2:** Review what Layer 0.5 is routing. Tune AGENT-PROMPT.md signal detection.
3. **Week 3:** Run migration script for specific files you're confident about.
4. **Week 4+:** Gradually move remaining files; remove `.migrated` copies.

This preserves continuity and gives you confidence before full cutover.

---

## Optional: Git Backup (Layer 2)

Add version control to your memory:

```bash
cd ~/.openclaw/workspace
git init
git remote add origin git@github.com:yourusername/yourrepo-memory.git
```

**Create `.gitignore`** (protect private files):
```gitignore
SOUL.md
USER.md
AGENTS.md
memory/daily/
SESSION-STATE.md
*.migrated
.env
```

**Daily backup cron (via OpenClaw):**
```json
{
  "name": "Layer 2 GitHub Backup",
  "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "America/Denver" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run: cd ~/.openclaw/workspace && git add -A && git commit -m 'daily backup: $(date +%Y-%m-%d)' && git push origin main",
    "model": "anthropic/claude-haiku-4-5",
    "timeoutSeconds": 60
  },
  "delivery": { "mode": "none" }
}
```

---

## Recovery Scenarios

### "Layer 0.5 stopped routing"

```bash
openclaw cron list              # find job ID
openclaw cron runs --job-id X   # check last run output
./scripts/template-integrity-check.sh  # verify AGENT-PROMPT.md
openclaw cron run --job-id X --run-mode force  # trigger manually
```

### "Memory files are empty / signals not routing"

1. Check WAL protocol is active (are you writing before responding?)
2. Check AGENT-PROMPT.md signal detection rules
3. Check workspace path is correct in AGENT-PROMPT.md
4. Force-run Layer 0.5 and check output

### "LCM database corrupted"

```bash
cp ~/.openclaw/lcm.db ~/.openclaw/lcm.db.backup-$(date +%Y%m%d)
rm ~/.openclaw/lcm.db
# Restart OpenClaw gateway (recreates clean database)
```

Layer 1 .md files are unaffected by LCM corruption.

### "Need to restore from backup"

```bash
# Git restore (if backup cron was running)
cd ~/.openclaw/workspace
git log --oneline | head -10
git checkout HEAD~1 -- memory/MEMORY.md  # restore specific file

# From migration backup
ls memory/migration-backup/
cp memory/migration-backup/2026-04-14-120000/MEMORY.md ./MEMORY.md
```

---

## VPS Persistent Volumes (Docker Deployments)

If running OpenClaw itself in Docker, ensure persistent volumes for both workspace and LCM:

```yaml
services:
  openclaw:
    image: openclaw/openclaw:latest
    volumes:
      - openclaw_workspace:/home/node/.openclaw/workspace
      - openclaw_data:/home/node/.openclaw
    ports:
      - "3000:3000"

volumes:
  openclaw_workspace:
  openclaw_data:
```

**Critical:** The `/home/node/.openclaw` volume must persist `lcm.db`, `openclaw.json`, and `auth-profiles.json`. Missing this volume mount is the most common cause of OpenClaw Docker deployment failures.

---

## Next Steps After Deployment

1. **Run for 1 week** — let Layer 0.5 operate autonomously
2. **Check `memory/self/`** — observe personality and identity development
3. **Add weekly reflection cron** — consolidate daily logs into `memory/reflections/weekly/`
4. **Add weekly introspection cron** — deep self-examination (narrative ID, growth, voice)
5. **Optional: Deploy Qdrant** — enable semantic search when memory grows
6. **Optional: Git backup** — add daily push for version control + recovery

---

*You now have a production-grade persistent memory system. Let it run.*
