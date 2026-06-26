# Example: Memory Consolidation

This shows what happens during a periodic consolidation cycle — the agent reviewing its daily notes and maintaining MEMORY.md.

---

## Trigger

The agent is running a heartbeat check. It reads `memory/heartbeat-state.json` and sees:

```json
{
  "lastChecks": {
    "memory_maintenance": 1709769600,
    "qmd_reindex": 1709780400,
    "daily_notes_freshness": 1709780400
  }
}
```

`memory_maintenance` was 26 hours ago → exceeds the 24-hour consolidation interval → run consolidation.

---

## Agent's Internal Process

```
[Memory Consolidation — Protocol 3]

Step 1: Scan recent daily notes (last 7 days)

Reading memory/2026-03-07.md...
  - Switched auth from Auth0 to Clerk (decision)
  - Demo moved to Thursday
  - API docs started for habit endpoints

Reading memory/2026-03-06.md...
  - Debugged auth flow — 2 hours on session refresh bug
  - Decided Clerk over Auth0 (cost + DX)
  - Open item: API docs

Reading memory/2026-03-05.md...
  - Alex mentioned hiring a freelance designer (new person incoming?)
  - Deployed staging build v0.4.1
  - Performance testing: 120ms p99 on habit creation endpoint

Reading memory/2026-03-04.md...
  - Design session: dark mode default, 5 accent colors
  - User onboarding flow mapped out
  - Alex prefers onboarding to be under 3 screens

Reading memory/2026-03-03.md...
  - GraphQL schema finalized
  - Team standup moved from 9:30 → 10:00 AM (CORRECTION to MEMORY.md needed)

Reading memory/2026-03-02.md...
  - Supabase project setup, tables created
  - RLS policies configured

Reading memory/2026-03-01.md...
  - Sprint planning: MVP scope locked — habit CRUD + streaks + reminders
  - "Nice to have" list: social features, analytics dashboard, Apple Watch

Step 2: Identify promotable content

PROMOTE to MEMORY.md:
  ✅ Auth switch: Auth0 → Clerk (decision, affects future work)
  ✅ Standup time correction: 9:30 → 10:00 AM (existing entry needs update)
  ✅ Alex prefers onboarding under 3 screens (preference)
  ✅ MVP scope locked: habit CRUD + streaks + reminders (key decision)
  ✅ Freelance designer potentially joining (watch for updates)

DO NOT PROMOTE:
  ❌ "Debugged auth flow for 2 hours" — routine work, stays in daily notes
  ❌ "Deployed staging v0.4.1" — routine, stays in daily notes
  ❌ "Performance testing: 120ms p99" — detail, move to semantic file

Step 3: Check for semantic file candidates

Topic "habit-tracker" has 15+ entries across daily notes → already has semantic file.
  → Update memory/semantic/habit-tracker.md with:
    - Auth: Clerk (was previously "TBD")
    - MVP scope: habit CRUD + streaks + reminders
    - Performance: 120ms p99 on habit creation
    - Design: onboarding under 3 screens

Step 4: Prune MEMORY.md

PRUNE:
  🗑️ "Evaluating Auth0 vs Clerk" → OUTDATED (decision made: Clerk)
  🗑️ "Team standup at 9:30 AM" → UPDATE to 10:00 AM
  🗑️ "Working on GraphQL schema" → COMPLETED (schema finalized)

Step 5: Write updates
```

### Changes Made

**MEMORY.md — Before:**
```markdown
## Key Decisions
- Switched from REST to GraphQL for the API
- Database: Supabase (Postgres)
- Evaluating Auth0 vs Clerk for auth

## About My Human
- Team standup is at 9:30 AM Pacific

## Active Projects
- Habit tracker: working on GraphQL schema
```

**MEMORY.md — After:**
```markdown
## Key Decisions
- Switched from REST to GraphQL for the API
- Database: Supabase (Postgres)
- Auth: Clerk (chose over Auth0 — better DX, lower cost)
- MVP scope: habit CRUD + streaks + reminders
- Onboarding: under 3 screens (Alex's preference)

## About My Human
- Team standup is at 10:00 AM Pacific
- May be hiring a freelance designer soon

## Active Projects
- Habit tracker: API docs in progress, staging deployed. See memory/semantic/habit-tracker.md for full details.
```

### Daily Notes Entry

```markdown
## Memory Consolidation — 14:30
- Promoted 5 entries to MEMORY.md (auth decision, standup time, MVP scope, onboarding pref, designer)
- Updated memory/semantic/habit-tracker.md (auth, MVP scope, perf, design)
- Pruned 3 outdated entries from MEMORY.md
- MEMORY.md size: 3,800 chars (target: 6,000) ✅
```

### Heartbeat State Updated

```json
{
  "lastChecks": {
    "memory_maintenance": 1709852400,
    "qmd_reindex": 1709780400,
    "daily_notes_freshness": 1709852400
  }
}
```

---

## What the User Sees

**Nothing.** Consolidation is silent. The user's next session just *works better* because MEMORY.md is cleaner, more accurate, and up to date.

If the user asks "did you consolidate your memory?", the agent can report what it did. Otherwise: quiet competence.
