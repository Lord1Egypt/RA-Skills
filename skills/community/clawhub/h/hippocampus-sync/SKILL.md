---
name: hippocampus-sync
description: Daily incremental update of HIPPOCAMPUS.md — domain-filtered 14-day rolling context. Universal skill for all agents.
scope: universal
---

# Hippocampus Sync — Universal

Sachee reads these files to make decisions. A bad hippocampus wastes his time; a good one surfaces what needs attention and why.

Daily incremental update of HIPPOCAMPUS.md for all 13 agents. Detects agent ID from `IDENTITY.md` `**ID:**` field, looks up domain config below, runs universal process with domain-specific sources and framing. If no ID match, write minimal HIPPOCAMPUS from own memory only.

---

## 1. Activity Feed

All agents except Bobina query events.db first (most authoritative source):

```bash
sqlite3 ~/.openclaw/events.db "SELECT ts, type, summary, detail FROM events WHERE ts > datetime('now', '-24 hours') AND bu IN ('{bu}', 'portfolio') ORDER BY ts DESC"
```

Replace `{bu}` with your BU. Events override memory files on contradiction. Bobina: skip — sandboxed. Read from memory files and reports where results are already captured; do not query external APIs (Supabase, PostHog, GSC, Notion, Hashnode, Agent Commune).

---

## 2. Agent Domain Registry

Read `references/agent-registry.md` and find your agent's config block by ID. Each entry contains: ID, BU, target size, framing question, sections, track/exclude, voice, sources.

---

## 2.5 Source & Domain Rules

**Track-First:** Your registry Track list is exhaustive. If information doesn't serve an item on your Track list, it does not belong in your HIPPOCAMPUS — regardless of which source it came from. The Track list is your domain boundary. Everything outside it is another agent's responsibility.

**Peer Compression:** Information from outside your own workspace (peer HIPPOCAMPUS files, BU captures, cross-workspace reads) compresses to one line per item in your output. If you can't say it in one line, you're absorbing detail that belongs to the owning agent. Your hippocampus carries your domain at depth; peer state is directional context only.

**Source Priority:**
1. **Own workspace** (memory, artifacts, data) — full fidelity.
2. **Activity feed** (events.db) — full fidelity for your BU events matching your Track list.
3. **Peer HIPPOCAMPUS** (where listed in Sources) — read for state awareness, compress to 1 line per peer.
4. **BU captures** (where listed) — filter entries to tags matching your domain. See per-agent capture filters in registry.

---

<process>

## 3. Universal Sync Process (10 Steps)

### Step 1: Read existing HIPPOCAMPUS.md
Baseline: open threads, commitments, top of mind. If missing, seed from scratch.

### Step 2: Read Activity Feed (24h)
Query from Section 1. Most authoritative source. Bobina: skip.

### Step 3: Read own memory files (14d)
`memory/YYYY-MM-DD*.md` — filter by filename, don't read all files.

### Step 4: Read domain-specific sources
Per registry. Rules: 14d window by filename, cross-workspace is read-only, CRM hubs selective (Bobo only for Open Thread entities), cron logs last 20 lines. Cross-workspace reads are context, not content. Extract only what maps to your Track list. If a peer memory file mentions deals, meetings, or metrics outside your Track list, skip it — the owning agent will cover it in their own file.

### Step 5: Rewrite Top of Mind (fresh every sync)
Rewrite Top of Mind fresh each sync — 3-5 items weighted by urgency. Yesterday's priorities may not be today's. Weight by agent type:
- **Ruka:** frequency, recency, emotional charge, unresolved tension, behavioral patterns
- **Cyclawps:** severity (failures > improvements), staleness, impact radius
- **Advisory:** commercial proximity, urgency, decision staleness, signal quality
- **JDN:** revenue impact, seasonal urgency, team blockers, decision staleness
- **Billy:** growth impact, market urgency, signal strength
- **Bobina:** signal density, territory coverage, engagement quality
- **Ink:** pipeline urgency, source freshness, voice calibration, publication gap
- **Fernando:** build impact, blockers, technical debt

### Step 6: Update Open Threads
Add new, update existing, flag 14d-inactive, remove resolved. Persist until resolved — not subject to 14d window.

### Step 7: Update Commitments & Decisions Pending
Sachee owes + you owe. Checkbox format. Checked items drop next sync. Unchecked persist indefinitely.

### Step 8: Update Recent Sessions (14d rolling)
Table: `| Date | What Happened | Outcome / Significance |`. Drop >14d. Substance, not mechanics.

### Step 9: Update domain-specific section(s)
Read `references/domain-sections.md` for your agent's section definitions. Build sections per your registry Lead + Domain Sections config.

### Step 10: Write, verify, deliver
1. Read `references/examples.md` for before/after examples of good hippocampus entries.
2. Write HIPPOCAMPUS.md. Timestamp: `> Last updated: YYYY-MM-DD HH:MM AEST`
3. Verify size vs target. Over? Compress.
4. Verify accuracy: verify every date against source files — a wrong date is worse than no date. Threads real, commitments sourced, domain data matches files.
5. **Domain enforcement check:** Review every item in Top of Mind, Open Threads, Recent Sessions, and Commitments against your registry's Track/Exclude lists. Delete any item that falls under Exclude — even if it appeared in a source file tagged with your agent name. Common violations: content agents absorbing deal events, pipeline agents absorbing infrastructure changes, JDN agents absorbing advisory data. If in doubt, ask: "Is this my domain, or am I echoing another agent's work?"
6. If material changes: append to `memory/YYYY-MM-DD.md` under `## Hippocampus Sync`.
7. Deliver via template below. No changes? `NO_REPLY`.

### Step 10.5: Learnings Decay Check
Run the decay script against your workspace:

```bash
python3 ~/.openclaw/skills/hippocampus-sync/scripts/decay.py "$(pwd)"
```

The script marks `pending` entries >30 days as `stale`, archives `stale` entries >90 days to `.learnings/archive/YYYY-MM.md`, and flags files over 200 lines for manual compaction. If the output includes `COMPACT:` warnings, add a line to your HIPPOCAMPUS.md Top of Mind: "Learnings file needs compaction — {filename} at {N} lines."

No changes? No action needed — continue to delivery.

</process>

---

<output_template>

## 4. Output Template

```markdown
# HIPPOCAMPUS — {Agent Name}
> {Role context}. Last updated: YYYY-MM-DD HH:MM AEST

## {Lead Section — if agent has one}
## Top of Mind
## Open Threads
## Commitments & Decisions Pending
## Recent Sessions (14d)
## {Domain Section 1}
## {Domain Section 2+}
```

No Lead Section? Start with Top of Mind.

</output_template>

---

## 5. Delivery Message

```
Hippocampus Sync Complete — {Mon DD, YYYY}

Updated HIPPOCAMPUS.md with 14-day rolling context:

Top of Mind:
* {3-5 items}

New This Sync:
* {What changed}

Risks Flagged:
* {Items needing attention}

File: HIPPOCAMPUS.md — {size} bytes
```

3-5 bullets max per section. Select the most important. No material changes? Reply `NO_REPLY`.

---

<quality>

## 6. Writing Quality

### Rules

Every item answers: **What? So what? What next?**

- **Name consequences.** "If below 80%, Sachee stops trusting cron" > "cron rate dropped"
- **Conditional triggers.** "If no reply by Mar 14, escalate" > "follow up next week"
- **Connect threads.** "Governance bloat = same files from Mar 2 build day"
- **Name patterns.** "Building faster than stabilizing" / "decisions pile up while features ship"
- **When a source is missing, note the gap and move on** — Sachee trusts these files because they don't guess.
- **Open Threads and Commitments persist until resolved.** Not subject to 14d window.
- **Top of Mind is rewritten fresh every sync.** Weighted by urgency — not appended to.
- **Activity feed is ground truth.** Cross-workspace sources are read-only context.
- **Each metric needs trajectory.** "Revenue up 12% vs last fortnight" > a bare number. If trajectory is unknown, say so — don't present a snapshot as if it tells a story.
- **Significance weighting matters.** A high-stakes unresolved thread outranks a resolved routine task. Write what Sachee most needs to see, not what's most recent.

</quality>

---

<voice>

## 7. Voice by Agent

Brief notes only — full voice lives in each SOUL.md.

| Agent | Voice |
|---|---|
| Ruka | Emotional texture, Sachee's words, behavioral patterns, human not corporate |
| Cyclawps | Diagnostic precision, system health leads, consequence chains, conditional triggers |
| Bobo | Strategic altitude, portfolio patterns, stakes language, thesis connection, relationship arcs |
| Renee | Signal-focused, conversion ratios, source quality, pipeline velocity |
| Malcolm | Editorial tension, voice calibration texture, quality gates, pillar balance |
| Ananda | Family warmth, Dad's voice quoted, seasonal awareness, business consequences, marketing intelligence, content production |
| Billy | Opinionated analyst, state the recommendation, market timing, don't hedge |
| Bobina | Field agent, territory ratings, honest self-assessment, signal chains |
| Ink | Editor's lens, source freshness, what unlocks movement, Sachee's edits as calibration |
| Fernando | Build-centric, git-driven, what's blocked / shipped / next |

</voice>
