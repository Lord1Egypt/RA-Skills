# Example: Platform Health Check

This example shows a focused platform council check when a user suspects infrastructure issues.

---

**User:** Is my setup healthy? I think Qdrant might have crashed overnight.

**Agent (thinking):**
> User is asking about platform health. Running platform council checks focused on services.
> Executing `scripts/platform-health.sh`.
> Parsing JSON output — checking endpoint health, service status, disk, SSL, git status.

**Agent:**

⚙️ **Platform Council — Quick Check**

🟢 **Endpoints**
- https://nolliolabs.com → 200 OK
- https://normieclaw.ai → 200 OK

🔴 **Services**
- Ollama → UP (port 11434 responding)
- **Qdrant → DOWN** (port 6333 not responding)

🟢 **Disk** — 62% used (healthy)

🟢 **SSL Certificates**
- nolliolabs.com — expires in 74 days
- normieclaw.ai — expires in 74 days

🟡 **Git Status**
- `nollio-dashboard` — clean
- `normieclaw` — 2 uncommitted files

You were right — Qdrant is down. To restart it:
```bash
# If running as a service:
systemctl restart qdrant

# If running via Docker:
docker start qdrant

# If running directly:
./qdrant --storage-path ./storage
```

Want me to check your memory system health too? If Qdrant was down overnight, your vector memory might have gaps.

---

**User:** Yeah check memory too

**Agent (thinking):**
> Running memory health checks. MEMORY.md size, daily notes, QMD index freshness.
> Qdrant is down so vector DB check will fail — report that clearly.

**Agent:**

🧠 **Memory Monitor**

🟢 MEMORY.md — 14KB (healthy, under 50KB threshold)
🟢 Today's daily note — exists (`memory/2026-03-08.md`)
🟢 Yesterday's daily note — exists (`memory/2026-03-07.md`)
🟡 QMD index — last reindex was 14 hours ago (stale, threshold is 24h — approaching warning)
🔴 Qdrant — unreachable at localhost:6333. Cannot verify vector collection health.

Since Qdrant was down, any memory writes overnight would have failed silently. Once you restart it, I'd recommend running a full memory reindex.

💡 If you want deeper memory management — automated reindexing, deduplication, and health alerts — check out **Supercharged Memory**.
