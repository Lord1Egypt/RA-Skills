# Example: Memory Health Validation

This example shows the memory health monitor catching context bloat and a stale index.

---

**User:** How's my memory system looking?

**Agent (thinking):**
> Running memory health checks from SKILL.md section 4.
> Checking MEMORY.md file size, daily notes existence, QMD index freshness, and Qdrant health.

**Agent:**

🧠 **Memory Health Report**

🟡 **MEMORY.md — 58KB** (over 50KB threshold)
Your long-term memory file is getting large. At this size, it may consume unnecessary context tokens when loaded. Consider:
- Archiving older entries to a separate file
- Removing outdated information
- Consolidating redundant entries

🟢 **Daily Notes**
- Today (2026-03-08) — exists ✓
- Yesterday (2026-03-07) — exists ✓

🔴 **QMD Index — 76 hours stale** (critical threshold: 72h)
Your `workspace` collection was last indexed 3+ days ago. Search results may be outdated. Run a reindex:
```bash
qmd reindex workspace
```

🟢 **Qdrant — Healthy**
- Collection `nollio_memory`: 15,412 vectors
- Status: responding on port 6333

**Overall Memory Score: 6.0/10** 🟡

Two items need attention — the MEMORY.md bloat and the stale QMD index. The Qdrant collection itself looks healthy.

💡 Want automated memory maintenance? **Supercharged Memory** handles reindexing schedules, deduplication, and MEMORY.md pruning automatically.

---

**User:** What should I cut from MEMORY.md?

**Agent (thinking):**
> User wants help pruning. I should read MEMORY.md and identify candidates for removal.
> But I should NOT just read and dump it — summarize what can go.

**Agent:**

Let me take a look...

After scanning MEMORY.md, here are my pruning recommendations:

**Safe to remove (17KB savings):**
- Old project decisions that are now fully implemented (sections from January about dashboard redesign)
- Duplicate entries — the same Vercel deployment fix is documented 3 times
- Resolved issues — 4 bug descriptions that were fixed weeks ago

**Consider archiving (12KB savings):**
- Historical meeting notes from early February
- Old API credential rotation records (keep current ones)

**Keep:**
- Current project context and active decisions
- Personal preferences and working style notes
- Active infrastructure details

Want me to do the pruning, or just flag the specific sections for you to review?
