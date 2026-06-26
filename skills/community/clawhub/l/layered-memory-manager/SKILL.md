---
name: layered-memory-manager
description: "Multi-tier (L1/L2) memory management skill for OpenClaw agents. Use when: (1) reading, writing, organizing, or searching memories, (2) deciding what to remember or forget, (3) performing memory hygiene (L1↔L2 sync, promotion, demotion), (4) answering questions about prior sessions, decisions, or preferences. Supports explicit forget (by tag or keyword), manual pin/promote via [[tag]] triggers, and memory_health status. This is the agent's own layered memory system — the authoritative guide for where memories live and how to keep them accurate."
---

# layered-memory-manager

> **Startup vs Hygiene mode**: The description above is your startup guide. Read the full skill below only when doing hygiene, maintenance, or architecture changes — not at every session boot.

## Memory Architecture

Memory is a **two-tier cache** system. Think L1 (hot) + L2 (cold).

**MEMORY.md = L1 Hot Cache**: Frequently accessed content stored inline for fast retrieval. Also serves as index to L2 files.

**memory/*.md = L2 Cold Storage**: Full detailed content lives here.

**hygiene.json = Access Tracker**: Located at `memory/hygiene.json` (workspace-relative). Tracks all access counts, promotions, and demotions.

```
MEMORY.md (L1 Hot Cache + Index)
├── [inline hot memories with metadata] ← frequently used, fast access
└── Layer Index                        ← pointer to L2 files

memory/*.md (L2 Cold Storage)
├── identity.md            ← full identity details
├── user.md               ← full user profile
├── preferences.md        ← all preferences
├── knowledge.md          ← stable facts, rules, experience
├── decisions.md          ← decisions with context
├── skills.md            ← installed skills
├── context.md            ← ongoing projects
├── hygiene.json          ← access tracking (NOT in a layer file)
└── YYYY-MM-DD.md         ← daily session logs

memory/archive/            ← archived cold content
```

### Layer Responsibilities

| Layer | L1 (Hot Cache) | L2 (Cold Storage) |
|---|---|---|
| Identity | Name, soul, core principles | Full personality details |
| User | Name, platform, language | Full user profile |
| Preferences | Core preferences | All preferences |
| Knowledge | Frequently accessed facts | Stable facts, rules, experience |
| Decisions | Recent key decisions | All decisions with context |
| Skills | Installed skills, usage principles | Detailed skill docs |
| Context | Ongoing projects | Full project details |
| Daily | — | Raw session logs |
| Hygiene | — | `hygiene.json` (tracked separately) |

## Retrieval Strategy

> These are behavioral guidelines, not rigid procedures. The goal is disciplined recall habits, not mechanical layering.

### Primary: Global `memory_search`
Use `memory_search` as the primary recall tool — it's fast and covers all layers.

### Secondary: Layer Awareness
When `memory_search` returns uncertain or partial results:
- Check MEMORY.md L1 hot cache for confirmed facts
- **Use `grep_search` on `memory/*.md`** for precise keyword or pattern matches in L2 (faster than full file reads)
- Check L2 file for full context
- Check daily logs if still unresolved

### When to Use `memory_get`
- `memory_search` or `grep_search` gave uncertain results and you need to verify exact content
- You know the file/location from context
- Confirming L1↔L2 sync state during hygiene check

### Behavioral Rules
- **Never assume** — always run `memory_search` before answering memory questions
- **Pre-decision Self-check (Mandatory)** — Before executing any tool that modifies the environment (e.g., `run_shell_command`, `replace`), **must** perform a quick `memory_search` or `grep_search` for relevant preferences or previous decisions. Never rely on model defaults if a project-specific memory might exist.
- **L1/L2 is binding** — L1 is a derived cache of L2; they are never independent. Any change to content always goes L2 first, then L1 resyncs. There is no such thing as editing L1 only.
- **Think in layers, not file scanning** — know which layer holds what; check L1/L2 when search gives weak signals


## L2 → L1 Promotion Mechanism

### Triggers

Promotion to L1 happens when content meets any of:

1. **Access frequency** — `hygiene.json` `accessLog[L2-key].sessions.length >= 3` (3+ unique sessions have accessed this L2 entry)
2. **Context criticality** — content is essential for every session (e.g., user name, core principles)
3. **User explicitly requests** — user says "remember this", "always keep in mind"
4. **Rapid re-access** — the same L2 content is needed twice in one session

### Promotion Process

1. Read full content from L2 file
2. Write condensed inline version to MEMORY.md under appropriate layer section
3. Keep L2 unchanged (source of truth stays intact)
4. Add promotion metadata tag to the L1 entry (see Tag Format below)
5. **Remove the entry from `accessLog`** — L2→L1 promotion is terminal for that L2 key; L1 access is tracked via the L1 section directly (promotionLog captures the event)
6. **After write: verify sync** — immediately read back the L2 file and confirm L1 condensation is still accurate. If L2 was edited mid-session, update or remove the L1 `↑` tag and re-promote fresh.

### Condensation Rules for L1

L1 inline content should be:
- **≤ 30 bullets total across all layers** (hard cap — see §L1 Global Budget)
- **Per-layer is a soft target** (~3–5 bullets) — not a hard ceiling; stay within global budget
- **Most representative** points only
- **No context or reasoning** — just facts/decisions
- If content can't be condensed, prioritize the top entries and note `→ Full version: memory/<layer>.md`

### Promotion Metadata Tag

Every L1 entry MUST carry a metadata tag. Format:

```
↑YYYY-MM-DD(<reason>)←<L2-source>[<flags>]
```

`<reason>` must be one of:
- `(N sessions)` — promoted after N cross-session accesses from hygiene.json `sessions` list
- `(user request)` — user explicitly asked to remember
- `(critical)` — context-critical, needed every session
- `(sync)` — L2 was edited; L1 re-condensed to match new L2 content

`<L2-source>` is the L2 key of the source file (see §L2 Key Format), e.g. `memory/decisions.md`. This field is mandatory — no tag is valid without it.

`<flags>` is optional; omit if none apply. Supported flags:
- `[pin]` — manually pinned via `[[pin:<layer>:<slug>]]`; never demoted by budget pressure

Examples:
- `↑2026-04-22(3 sessions)←memory/decisions.md` — promoted after 3 cross-session accesses
- `↑2026-04-22(user request)←memory/preferences.md[pin]` — promoted and manually pinned
- `↑2026-04-22(critical)←memory/identity.md` — context-critical, needed every session
- `↑2026-04-22(sync)←memory/decisions.md` — L2 was edited; L1 re-synced

**Tag integrity rule:** Because L1 and L2 are bound, the `↑` tag date is the date of the last L2→L1 sync. After any L2 edit, the corresponding L1 tag must be updated to today's date with reason `(sync)`.

### L1 Global Budget & Eviction Priority

**Hard cap: ≤ 30 bullet points total across all hot layers.**

Entries are evicted in priority order — lowest priority evicted first:

| Priority | Label | Rule | Never demoted |
|---|---|---|---|
| 1 | 🔒 critical | Tagged `↑(critical)` by system | ✅ yes |
| 2 | 📌 pinned | Tagged `↑[pin]` manually or via `[[pin:<layer>:<slug>]]` | ✅ yes |
| 3 | 🔥 recent | `sessionsSinceAccess == 0` (accessed this or last session) | ❌ no |
| 4 | ⏳ stale | `sessionsSinceAccess == 1–2` (skipped 1–2 sessions) | ❌ no |
| 5 | ❄️ cold | `sessionsSinceAccess >= 3` OR tagged `[[forget:<layer>:<slug>]]` | ❌ no |

**Eviction order:** cold → stale (oldest first) → recent (oldest first). Tiers 1–2 are exempt.

During overflow, demote lowest-priority entries first. If priority ties, demote the one with the highest `sessionsSinceAccess`. If still tied, demote the oldest by `↑` promotion date.

### Example: Promoting a Decision

**L2** `memory/decisions.md`:
```markdown
- 2026-04-22: Restructured memory into two-tier architecture
  - Reason: Layering makes retrieval faster, MEMORY.md acts as hot cache
  - Discussion: User proposed this design, I agreed with the approach
```

**L1** MEMORY.md Decisions section:
```markdown
## 📋 Decisions (Hot Cache)
- 2026-04-22: Restructured memory into two-tier architecture (hot cache + L2) ↑2026-04-22(3 sessions)←memory/decisions.md
→ Full version: `memory/decisions.md`
```

## L1 → L2 Demotion Mechanism

### Observable Triggers

Demotion from L1 happens when ANY of the following is **directly observable**:

1. **Zero-access demotion** — this L1 entry was NOT queried (`memory_search` hit it) for the last **3 consecutive sessions**
2. **Size overflow** — L1 total exceeds ~30 bullets; demote lowest-priority entries
3. **User explicitly updates preference** — user changes something; update L2, then sync L1
4. **Context expiry** — an entry was promoted for a temporary context (e.g., project X) and that context is now finished

> **Note on staleness:** Because L1/L2 are always bound, staleness is not a separate demotion trigger — it is handled automatically via sync. If L2 changes, L1 always resyncs immediately (not demoted). The `↑` tag date reflects the last sync.

### Tracking: sessionsSinceAccess (L1 entries)

L1 entries are tracked in `hygiene.json` `L1accessLog`:

```json
{
  "L1accessLog": {
    "<layer>:<slug>": {
      "sessionsSinceAccess": 0,
      "lastAccess": null,
      "lastSessionId": null,
      "pinned": false
    }
  }
}
```

**Session-start increment (mandatory, every new session):**

1. Call `session_status` to get the current session ID
2. For each L1 entry in `L1accessLog`:
   - If `lastSessionId` is NOT equal to the current session ID → `sessionsSinceAccess++`
   - If `sessionsSinceAccess >= 3` → mark for demotion (❄️ cold tier)
3. Save updated `hygiene.json`

**On every L1 entry access** (any `memory_search` hit or direct read within the current session):
→ `L1accessLog[entry].sessionsSinceAccess = 0`
→ `L1accessLog[entry].lastAccess = <today>`
→ `L1accessLog[entry].lastSessionId = <current session ID>`

**Key:** A single long session accessing the same entry 50 times counts as 1 session of access, not 50. Entries not accessed during the previous session are the only ones that accumulate `sessionsSinceAccess`.

**L2 entries use `accessLog`** (separate tree):
```json
{
  "accessLog": {
    "<L2-key>": {
      "accessCount": 0,
      "sessions": [],       // unique session IDs that accessed this L2 entry
      "lastAccess": null
    }
  }
}
```
On L2 access: if `sessionId` not already in `sessions`, push it → `accessCount = sessions.length`, `lastAccess = today`. The promotion trigger checks `accessCount >= 3`, where each increment requires a **different session** — a single session accessing the same L2 entry 10 times still counts as 1.
On L2→L1 promotion: **remove from `accessLog`** (promotion is terminal).

### Demotion Process

1. **Do NOT delete L2** — L2 is always the source of truth
2. Remove the inline content from MEMORY.md hot cache section
3. Add a reference note in MEMORY.md layer section pointing to full L2 content
4. Log the demotion in `hygiene.json` `demotionLog`
5. Update `L1accessLog` — remove the entry (it's now cold)
6. **Re-initialize `accessLog`** — the content is back in L2 cold storage with `accessCount: 0, sessions: [], lastAccess: null` (promotion history lives in `promotionLog`; re-promotion will trigger naturally from fresh accesses)

### Demotion ≠ Deletion

Demotion means "remove from hot cache", not "delete". L2 always retains the full version.
The goal is keeping L1 lean and accurate, not reducing total memory.

### Staleness Detection

Because L1/L2 are always binding, staleness is handled by **sync, not demotion**:

```
FOR each L1 layer section:
  READ L2 file for that layer
  FOR each L1 bullet with ↑YYYY-MM-DD tag:
    IF L2 was modified AFTER ↑date:
      → re-condense L2 content → update L1 with ↑today(sync)←<L2-source>
    ELSE IF L2 has content not in L1:
      → re-condense and promote (add ↑today(sync))
```

Only entries that are genuinely cold (3+ sessions with no access) should be **demoted** — not ones whose L2 source changed.

### L2 Key Format

Every entry in `accessLog` and `promotionLog` / `demotionLog` uses the key format:

```
memory/<layer>.md:<slug>
```

- `<layer>` is the layer name (e.g. `decisions`, `preferences`)
- `<slug>` is a short, unique identifier for the entry within that file — use a URL-safe slug derived from the entry topic or first line (e.g. `two-tier-architecture`, `preferred-package-manager`)
- Example: `memory/decisions.md:two-tier-architecture`

This format lets you directly map any hygiene log entry back to its source file.

## hygiene.json Schema

```json
{
  "L1accessLog": {
    "<layer>:<slug>": {
      "sessionsSinceAccess": 0,
      "lastAccess": null,
      "lastSessionId": null,
      "pinned": false
    }
  },
  "accessLog": {
    "<L2-key>": {
      "accessCount": 0,
      "sessions": [],
      "lastAccess": null
    }
  },
  "promotionLog": [
    { "entry": "<L2-key>", "from": "L2", "to": "L1", "at": "YYYY-MM-DD", "reason": "..." }
  ],
  "demotionLog": [
    { "entry": "<L2-key>", "from": "L1", "to": "L2", "at": "YYYY-MM-DD", "reason": "..." }
  ],
  "archiveQueue": []
}
```

> **Note:** `hygiene.json` lives at `memory/hygiene.json` (workspace-relative), NOT inside the skill directory.

## Manual Tag Triggers

User can embed directive tags in messages. These are detected and acted upon during session processing — no cron needed.

### `[[pin:<layer>:<slug>]]`
Pin a L1 entry so it becomes Tier 2 (never demoted by budget pressure).
- Add `↑[pin]` to the entry's metadata tag, e.g. `↑2026-04-22(3 sessions)←memory/decisions.md[pin]`
- Persist `↑[pin]` in both L1 and L2 source
- Update `L1accessLog[entry].lastAccess = today`
- Layer index: `memory/<layer>.md:<slug>`

### `[[promote:<layer>:<slug>]]`
Force-promote a L2 entry to L1 immediately (bypasses 3-session threshold).
- Read full content from L2
- Condense and write to L1 with `↑YYYY-MM-DD(user request)←<L2-source>`
- Log to `promotionLog`
- Remove from `accessLog` (or reset: accessCount → 0, sessions → [], lastAccess → null)

### `[[forget:<layer>:<slug>]]`
Demote a L1 entry back to L2 cold storage immediately.
- Remove L1 inline content
- Keep L2 source intact
- Log to `demotionLog`
- Remove from `L1accessLog`
- Re-initialize `accessLog` for that entry (accessCount: 0, sessions: [], lastAccess: null)

### `[[forget keyword:<word>]]`
Forget any entry whose slug or content contains `<word>` — case-insensitive substring match across L1 and L2.

**Match semantics:**
- Case-insensitive (`jarvis` matches `Jarvis`, `JARVIS`)
- Substring match on both entry slug and full content
- Matched as continuous substrings (e.g., `two-tier` matches `two-tier-architecture`, not `two` alone)
- Delimiters (space, `-`, `_`, `.`) are included but do not break the match
- L1 bullet matched → demote that entry immediately
- L2 file content matched → also demote the corresponding L1 entry if one exists
- Report how many entries were forgotten after completing the scan

### `[[restore:<layer>:<slug>]]`
Restore an archived entry back to active L2 storage.
- Search `memory/archive/` for the entry matching the slug.
- Re-insert the content into `memory/<layer>.md`.
- Remove from `archiveQueue` in `hygiene.json`.
- Initialize `accessLog[entry]` with `accessCount: 1` (to account for the restoration access).
- **Optional Promotion:** If the user specifies (e.g., "restore and pin"), also promote to L1.

## `[[memory_health]]` — Status Snapshot

Called on demand (not on heartbeat). Output format:

```
=== Memory Health ===
L1: <N>/30 bullets | <M> tagged [pin]
L2: <X> files | <Y> entries tracked
Promotions (total): <P>
Demotions (total): <D>
Archive queue: <A> items
===
Priority breakdown:
  🔒 critical: <n>  📌 pinned: <n>  🔥 recent: <n>  ⏳ stale: <n>  ❄️ cold: <n>
===
L2 cold candidates (never accessed, age>30d): <C>
L1↔L2 sync (L1 has stale L2 source): <s>
===
Log Cleanup:
  Log items over 180 days pruned from hygiene.json: <L>
===
Top L1 entries by sessionsSinceAccess:
  1. <layer>:<slug> — <n> sessions stale
  2. ...
```

Note: `L2 cold candidates` measures L2 entries that have never been accessed (`accessCount==0`) and are older than 30 days — candidates for archive. `L1↔L2 sync` measures L1 entries whose L2 source has been modified since promotion — these need re-evaluation.

## Archive / Forgetting Mechanism

### Archive Triggers

1. **Cold L2**: use the **earlier** of file creation date and last access date as the baseline:
   - If `lastAccess == null` and file mtime is 30+ days old → archive candidate
   - If `lastAccess != null` and days since `lastAccess >= 30` → archive candidate
   - If `accessCount == 0` (never accessed at all) and file is new, no action yet — wait for the 30-day window to close before treating as cold
2. **Post-demotion cold storage**: an entry was demoted from L1 and has had **0 re-access for 60 days** in L2
3. **User explicitly discards**: user says "forget about X" or "delete X" → move to archive, never delete outright

### Archive Process

1. Move content from `memory/<layer>.md` to `memory/archive/<layer>-<date>.md`
2. Add entry to `hygiene.json` `archiveQueue` with `{entry, archivedAt, reason}`
3. Update `memory/<layer>.md` — remove the content, add a comment noting it's archived
4. Log to `memory/decisions.md` or today's daily log
5. **Proactive Search Notice:** If future tasks trigger an archive search, notify the user about the existence of relevant archived entries.

### Archive Review & Log Pruning

During heartbeat hygiene, if `archiveQueue.length > 0`, check each item:
- If archived > 180 days ago and never restored → permanently delete from archive (optional, user can confirm)
- Otherwise leave in archive indefinitely

**Hygiene Log Pruning:** To prevent `hygiene.json` from becoming a performance bottleneck:
- Prune `promotionLog` and `demotionLog` entries older than 180 days.
- Ensure the file is kept under ~50KB. If larger, archive old log entries into `memory/archive/hygiene-log-YYYY-MM.json`.

## Write Strategy (Cache Coherence)

### Write Order (Enforced)

1. **Write to L2 first** — L2 is always source of truth
2. **Sync L1 immediately** — update hot cache to match L2, add new `↑` tag with today's date and reason
3. **Update hygiene.json** — update the relevant accessLog (L1accessLog or accessLog), reset counters

### Sync Verification

**Write L2 first, then sync L1.** Because they are binding, this order is always enforced:

1. Write new/updated content to L2 (source of truth)
2. Immediately re-condense and update the corresponding L1 entry with `↑today(<reason>)←<L2-source>`
3. Verify: read back L2 and confirm L1 condensation is accurate

After any L2 update:
```
READ MEMORY.md corresponding layer
IF L1 section does NOT reflect the change:
  → re-condense L2 content and write to L1 with ↑today(sync)←<L2-source>
```

## When to Activate This Skill

### Before Answering Memory Questions
Any question about past sessions, decisions, preferences, or facts → `memory_search` first, then L1/L2 as needed.

### After Significant Events
- User says "remember this" or "don't forget"
- Made a decision that should persist
- Learned something new about the user or environment
- Completed a project or milestone
- Opened or closed a project / context

### Manual Tag Triggers (user-embedded)
Detect and process `[[pin:<layer>:<slug>]]`, `[[promote:<layer>:<slug>]]`, `[[forget:<layer>:<slug>]]`, `[[forget keyword:<word>]]`, or `[[memory_health]]` tags in user messages — act on them during the same turn.

### When Creating or Editing Skills
Align new skill structure with memory architecture. Update `memory/skills.md` when skills are installed or removed.

### During Hygiene Maintenance
Run the Hygiene Checklist (defined below) when maintenance is needed.

## Hygiene Checklist

Run during periodic maintenance. Keep it light — focus on what actually changed since last run:

```
1. CHECK L1 budget: count bullets — if approaching ~30:
   demote ❄️ cold → ⏳ stale (oldest first) → 🔥 recent (oldest first)
   skip 🔒 critical and 📌 pinned entries regardless of age
2. SYNC check: for each L1 entry with ↑ tag, compare ↑date with L2 mtime
   - L2 newer than ↑date → re-condense L2 and update L1 tag to ↑today(sync)
   - L2 has new content not in L1 → re-condense and promote (add ↑today(sync))
   (Note: no demotion here — L2 being newer means L1 needs to catch up, not go away)
3. CHECK accessLog:
   - Any L2 entry `accessCount >= 3` (check `sessions.length`) and still in L2? → promote to L1
4. CHECK archiveQueue:
   - Any L2 entry cold for 30+ days? → move to memory/archive/
   - Any archived > 180 days? → surface for permanent-deletion confirmation
5. CHECK post-demotion cold storage:
   - Any demoted L1 entry in L2 with 0 re-access for 60+ days? → add to archiveQueue
6. SAVE hygiene.json with all updated logs
```

## Recovery: Rebuilding hygiene.json

### If `hygiene.json` is lost or corrupted:

1. **Read MEMORY.md** — extract all L1 entries with their `↑` tags → rebuild `L1accessLog` (all entries start with `sessionsSinceAccess: 0`)
2. **Read all L2 files** → for each entry, initialize `accessLog` with `accessCount: 0, sessions: [], lastAccess: null`
3. **Preserve `promotionLog` and `demotionLog`** from the corrupted file if any survived; if fully gone, reconstruct from L1 `↑` tags and daily logs
4. **Recreate hygiene.json** with recovered data + current date

> **Known recovery cost:** All cross-session access history resets to 0. L2 entries approaching the 3-session promotion threshold must re-accumulate from scratch. Accept this as unavoidable without persistent session logs.

### If `MEMORY.md` is lost:

1. **Read all L2 files** → rebuild L1 by condensing the most important content (≤ 5 bullets per layer, priority: Identity > User > Preferences > Decisions > Knowledge > Skills > Context)
2. **Use `promotionLog`** to re-promote known-hot entries first
3. **Restore `L1accessLog`** with all `sessionsSinceAccess: 0`

## Critical Rules

- **MEMORY.md is private** — never load or mention in group chats
- **L1/L2 are binding** — no such thing as editing one without the other. Write L2 first, then sync L1. Never edit L1 directly.
- **L2 is source of truth** — never delete L2 content directly; archive first
- **Keep L1 and L2 in sync** — the `↑` tag date is always the last sync date; never leave a stale tag
- **Promote at accessCount >= 3** — use the counter, not guesswork
- **Tag everything** — no untagged L1 entries; `↑` metadata is mandatory
- **Log all changes** — hygiene.json tracks everything; no untagged state changes
- **Archive, don't delete** — cold content goes to `memory/archive/`, not trash

## Storage Patterns

### Adding a New Layer
1. Create `memory/<layer>.md`
2. Write full content to L2
3. Condense and write the L1 entry in MEMORY.md with `↑YYYY-MM-DD(new layer)←memory/<layer>.md`
4. Update MEMORY.md Layer Index
5. Initialize `accessLog[<layer>:<slug>]` in hygiene.json (accessCount: 0, lastAccess: null)

### Daily Session Logging

Write to `memory/YYYY-MM-DD.md`. Use this minimal template:

```markdown
# YYYY-MM-DD

## Summary
<!-- 3-5 summary items -->

## Key Outcomes
<!-- Decisions, commitments, and things to remember -->

## Notes
<!-- Items worth recording but not yet ready for L2 promotion -->
```

After the session ends, distill key outcomes into L2 layer files and sync important content to L1 as needed.

### Archive Directory
```
memory/archive/
├── decisions-2026-01-15.md   ← cold decision, archived
├── context-projectX-2026-03-01.md
└── ...
```
Archive files keep the original content intact for potential restoration.
