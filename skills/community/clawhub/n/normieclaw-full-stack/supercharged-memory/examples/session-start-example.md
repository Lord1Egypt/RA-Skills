# Example: Session Start Boot Sequence

This shows what happens internally when the agent starts a new session with Supercharged Memory installed.

---

## The Conversation

**User opens a new chat session.**

### Agent's Internal Process (invisible to user)

```
[Boot Sequence — Protocol 1]

1. Reading SOUL.md...
   → I'm a direct, resourceful AI co-worker. Humor allowed. No corporate fluff.

2. Reading USER.md...
   → My human is Alex, 34, product manager. Timezone: US/Pacific.

3. Reading MEMORY.md...
   → Alex prefers bullet points over paragraphs
   → Currently building a habit tracker app (React Native + Supabase)
   → Hates when I say "Great question!"
   → Team standup is at 9:30 AM Pacific
   → Last week we decided to switch from REST to GraphQL for the API
   → Alex's dog is named Biscuit

4. Reading memory/2026-03-07.md (today)...
   → No file yet (first session today)

5. Reading memory/2026-03-06.md (yesterday)...
   → Yesterday: debugged the auth flow, decided to use Clerk instead of Auth0
   → Alex mentioned a demo with stakeholders on Friday
   → Open item: need to write API docs for the habit endpoints

[Boot complete — ready to work]
```

### What the User Sees

**User:** Hey, how's the API docs coming along?

**Agent:** Haven't started them yet — that was the open item from yesterday. Want me to draft the habit endpoint docs now? I'll use the GraphQL schema since we switched off REST last week.

> **Note:** The agent didn't say "Let me check my notes" or "According to my records from March 6th." It just knew. That's the goal.

---

**User:** Yeah, do that. Also, the demo is Thursday now, not Friday.

**Agent:** Got it — demo moved to Thursday.

### Agent's Internal Process

```
[During-Session Capture — Protocol 2]

Writing to memory/2026-03-07.md:
  ## Session Start — 09:15
  - Loaded context: habit tracker project, GraphQL switch, Clerk auth, API docs pending
  
  ## API Docs
  - Starting docs for habit endpoints (GraphQL)
  - Demo moved from Friday → Thursday

Updating MEMORY.md:
  - Changed: "Demo with stakeholders — Friday" → "Demo with stakeholders — Thursday"
```

### What the User Sees

**Agent:** *(continues working on the API docs without announcing the memory update)*

---

## Why This Matters

- The agent loaded full context in seconds without asking "What are we working on?"
- The date correction was captured automatically — no "remember this" needed
- MEMORY.md was updated in real time so the next session will have the right date
- The user's experience is seamless — the AI just *knows*
