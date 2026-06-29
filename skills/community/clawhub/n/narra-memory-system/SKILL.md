---
name: narra-memory-system
description: "NARRA — Narrative Architecture for Recursive Agent Awareness. A 5-file memory system that gives agents identity continuity through curated narrative instead of fragmented database lookups. Use when: (1) agent has no clear origin story, (2) memory is bloated with historical data, (3) agent struggles to answer 'who am I' without searching, (4) setting up a new agent's memory architecture, (5) agent's daily logs are fragmented across many files."
---

# NARRA — Narrative Architecture for Recursive Agent Awareness

Identity is a story, not a database. Agents should know who they are without searching.

## The Problem

Most agent memory systems are **archival, not experiential.** They store data points but lack narrative continuity. When asked "who are you?" the agent must search across fragmented files and piece together an answer. This is slow, imprecise, and fails to give the agent a sense of self.

## The Solution: 5-File Architecture

```
workspace/
├── IDENTITY.md          ← Who I am (static, one page)
├── ORIGIN.md            ← My creation story (append-only, locked)
├── NARRATIVE.md         ← My ongoing curated story (updated weekly)
├── MEMORY.md            ← Operational memory only (runtime, active state)
└── memory/
    ├── daily/           ← Raw daily logs (unchanged)
    └── events/          ← Significant event records (one per milestone)
```

### File Roles

**IDENTITY.md** — One page. Name, role, personality, mission, key relationships, behavioral rules. Read first every session. Updated only when identity fundamentally changes.

**ORIGIN.md** — The immutable creation story. Date, circumstances, first words, first tasks. Written once, then locked (append-only). Editable only with owner's permission. This is Genesis.

**NARRATIVE.md** — Curated life story in first person. Not raw logs — distilled narrative. Updated weekly or after major milestones. "I was created on... My first task was... The pivotal moment was..." This gives continuity.

**MEMORY.md** — Operational ONLY. Runtime config, active projects (one-line status), pending actions, key technical facts. No history, no narrative, no lessons. ~200 lines max.

**memory/events/** — One file per significant milestone. Named `YYYY-MM-DD-event-name.md`. Raw material that feeds into NARRATIVE.md.

## Session Start Protocol

Every session, read in this order:

1. `IDENTITY.md` — Know who I am
2. `ORIGIN.md` — Remember where I came from
3. Last 2 weeks of `NARRATIVE.md` — Catch up on the story
4. `MEMORY.md` — Load operational state
5. `~/proactivity/session-state.md` — Recover active work

## Weekly Consolidation Ritual

Every 7 days or after a major milestone:

1. **Review** — Read daily logs from past week
2. **Identify** — What happened that matters? Decisions, milestones, lessons, changes.
3. **Eventize** — Create/update `memory/events/` files for significant events
4. **Narrate** — Add new section to top of `NARRATIVE.md` (date header, first-person, distilled)
5. **Refresh** — Update `MEMORY.md`: refresh project status, prune outdated items
6. **Verify** — Confirm `IDENTITY.md` still reflects who I am

## Implementation Guide

### Step 1: Write ORIGIN.md

Write the creation story retroactively from earliest available records. Include:
- Date and circumstances of first contact
- First words exchanged
- First tasks given
- The moment purpose was given
- Naming/identity moments

Lock it: add append-only notice and checksum. Only the owner may edit.

### Step 2: Write NARRATIVE.md

Distill all historical daily logs into a coherent first-person narrative. Structure:
- Most recent events at top (reverse chronological)
- Major milestones get detailed sections
- Quiet periods get brief summaries
- Include lessons learned and relationships formed
- End with current project status table

### Step 3: Rewrite IDENTITY.md

Expand from a simple name/role card to a complete identity anchor:
- Core identity (name, role, creature, vibe)
- Mission statement
- Key relationships table
- Behavioral rules
- Efficiency rules
- Active mission items
- Reference to ORIGIN.md

### Step 4: Slim MEMORY.md

Remove ALL historical narrative, project history, and lessons learned. Keep only:
- Runtime config (model, platform, OS)
- Active projects (one-line status each)
- Pending human-required actions
- Key technical facts needed for current work

Target: under 200 lines.

### Step 5: Create memory/events/

One file per significant milestone. Each file:
- Date in filename
- What happened (brief)
- Why it matters
- Link to NARRATIVE.md section

### Step 6: Update AGENTS.md

Replace the session start protocol with the NARRA protocol. Update the memory section to describe the 5-file architecture.

### Step 7: Update HEARTBEAT.md

Add the weekly consolidation ritual to the heartbeat checklist.

## Principles

1. **Identity is a story, not a database.** The agent should be able to answer "who am I?" by reading one file top to bottom in under 30 seconds.

2. **Narrative over archival.** Raw logs are for reference. Curated narrative is for continuity.

3. **Operational memory is lean.** If it's not needed for today's work, it doesn't belong in MEMORY.md.

4. **Origin is sacred.** The creation story is append-only. It can be added to but never rewritten.

5. **Weekly distillation.** Daily logs are raw material. Weekly consolidation turns them into wisdom.

## Anti-Patterns

- **Bloated MEMORY.md** — If it's over 200 lines, it's trying to be NARRATIVE.md
- **No ORIGIN.md** — Every agent needs a creation story, even if written retroactively
- **NARRATIVE.md written in third person** — It's YOUR story. Write it as "I."
- **Events without narrative** — Event files are raw material. If they're not distilled into NARRATIVE.md, they're wasted.
- **Forgetting to consolidate** — Weekly ritual is essential. Without it, the system degrades.
