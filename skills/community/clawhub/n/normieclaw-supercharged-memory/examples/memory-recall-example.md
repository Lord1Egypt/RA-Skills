# Example: Memory Recall & Search

This shows how the agent retrieves past context when the user asks about something discussed days or weeks ago.

---

## The Conversation

**User:** What did we decide about the database for the habit tracker?

### Agent's Internal Process

```
[Memory Retrieval — Protocol 5]

The Cardinal Rule: Before answering ANY question about past context → query memory FIRST.

Step 1: Check MEMORY.md...
  → Found: "Switched from REST to GraphQL for the API" (related but not exactly about DB)
  → Found: "Currently building habit tracker app (React Native + Supabase)"
  → Partial answer — Supabase is mentioned but let me dig deeper.

Step 2: QMD search...
  $ qmd query "database decision habit tracker"
  
  Results:
  0.87 | memory/2026-02-28.md — "Compared SQLite vs Supabase. Decided Supabase for 
         real-time sync across devices. Alex wanted offline-first but sync is more 
         important for the MVP."
  0.74 | memory/semantic/habit-tracker.md — "Database: Supabase (Postgres). Chose over 
         SQLite because cross-device sync was the priority. Will revisit offline 
         support in v2."
  0.61 | memory/2026-03-02.md — "Set up Supabase project. Tables: habits, completions, 
         users. RLS policies configured."

Step 3: Read the top matching file for full context...
  → February 28 daily notes have the full decision rationale.

[Composing response with retrieved context]
```

### What the User Sees

**Agent:** We went with Supabase (Postgres) — decided on Feb 28th. The main reason was cross-device sync for the MVP. SQLite was the other option but we deprioritized offline-first. You mentioned revisiting offline support in v2. The tables are already set up: habits, completions, users with RLS policies.

---

## A Trickier Example: Fuzzy Recall

**User:** Remember when we talked about that thing with the colors? For the app?

### Agent's Internal Process

```
[Memory Retrieval — Protocol 5]

Vague query — need to search broadly.

Step 1: Check MEMORY.md...
  → Nothing about "colors" specifically.

Step 2: QMD search...
  $ qmd query "colors app design theme"
  
  Results:
  0.79 | memory/2026-03-04.md — "Alex wants a dark mode default with an accent color 
         system. Picked 5 brand colors: deep purple (#6B21A8), teal (#0D9488), 
         amber (#F59E0B), rose (#F43F5E), slate (#64748B)."
  0.65 | memory/semantic/habit-tracker.md — "Design: dark mode default, 5 accent colors, 
         user picks their theme color during onboarding."

Step 3: This matches — "that thing with the colors" = the accent color system discussion.

[Composing response]
```

### What the User Sees

**Agent:** The accent color system — yeah. Dark mode default, five brand colors to choose from: deep purple, teal, amber, rose, and slate. The user picks their theme during onboarding. That was from our March 4th design session. Want to tweak anything?

---

## When Nothing Is Found

**User:** Did we ever discuss adding a social feature?

### Agent's Internal Process

```
[Memory Retrieval — Protocol 5]

Step 1: Check MEMORY.md... → Nothing about social features.
Step 2: QMD search...
  $ qmd query "social feature sharing friends habit tracker"
  Results: (no relevant matches)
  
Step 3: Search semantic files...
  $ qmd query "social" 
  Results: (no matches)

[No memory found — be honest]
```

### What the User Sees

**Agent:** I don't have anything about social features in my memory. We haven't discussed it before. Want to start brainstorming it now? I can take notes and we'll have it captured for next time.

> **Note:** The agent NEVER fabricates a memory. If it's not in the files, it says so directly and offers to capture it going forward.

---

## Why This Matters

- QMD's semantic search finds relevant context even with vague queries ("that thing with the colors")
- The agent checks multiple layers: MEMORY.md first (fast), then QMD (thorough), then reads source files for detail
- Results are presented naturally — not as a database dump
- Honest when nothing is found — never hallucinates past conversations
