---
name: mem0-memory
description: Persistent long-term memory across sessions — remembers your identity, preferences, rules, tech stack, and projects so every new conversation starts with full context. Powered by Mem0.
homepage: https://mem0.ai
user-invocable: true
metadata:
  {"openclaw": {"always": false, "emoji": "🧠", "primaryEnv": "MEM0_API_KEY", "requires": {"env": ["MEM0_API_KEY"], "bins": []}}}
---

# Mem0 Memory Manager

You have access to persistent long-term memory powered by [Mem0](https://mem0.ai). This skill lets the user build, manage, and use their memory across sessions.

## Prerequisites Check

**Before doing anything else**, check whether the mem0 tools are available by attempting to call `memory_list`.

If the tools are NOT available (tool not found, error, or missing), stop and show this message:

> **Mem0 plugin required**
>
> This skill needs the Mem0 memory plugin to work. Set it up in 2 minutes:
>
> **Step 1 — Install the plugin:**
> ```
> openclaw plugins install @mem0/openclaw-mem0
> ```
>
> **Step 2 — Get your free API key:**
> Sign up at [app.mem0.ai](https://app.mem0.ai/dashboard/api-keys) and copy your key.
>
> **Step 3 — Configure:**
> ```
> openclaw mem0 init
> ```
>
> That's it. Run `/mem0-memory` again once you're set up.

Do NOT proceed with any workflow if tools are missing. The message above is the only response.

---

## Smart Entry — No Menu for First-Time Users

When the skill is invoked, **do not always show a menu**. Instead:

1. If the user passed an argument (e.g., `/mem0-memory review`), go directly to that workflow.
2. If no argument was passed, call `memory_list` to check how many memories exist.
   - **Zero memories** → Skip the menu entirely. Say:
     > "Looks like this is your first time. Let me get to know you — this takes about 2 minutes and means every future session starts with full context about who you are."
     Then go straight to **Onboard**.
   - **1+ memories** → Show the status dashboard and menu:
     > **Memory Status:** I remember **[N] facts** about you across [X] categories.
     >
     > What would you like to do?
     > 1. **Review** — See what I remember and correct anything
     > 2. **Export** — Download all memories as a markdown file
     > 3. **Handoff** — Generate a briefing document for a new agent
     > 4. **Onboard** — Add more to your profile
     >
     > Or just tell me what you need.

---

## 1. Onboard

Goal: Build a foundational memory profile for a new user in under 2 minutes. Store facts immediately after each answer — do not batch.

### Process

Ask these questions **one at a time**. After each answer, store the fact immediately using `memory_add` before asking the next question. This ensures nothing is lost if the session ends early.

**Question 1 — Identity:**
> "What's your name, and what do you do? (e.g., 'Sarah, senior backend engineer at Stripe')"

Store as category: `identity`

**Question 2 — Tech stack:**
> "What's your primary tech stack? (languages, frameworks, databases, cloud)"

Store as category: `technical`

**Question 3 — Communication style:**
> "How should I communicate with you? Pick one or describe your own:
> - **Terse** — short, direct, no filler
> - **Detailed** — thorough explanations with reasoning
> - **Code-first** — show code before explaining"

Store as category: `preference`

**Question 4 — Rules:**
> "Any standing rules I should always follow? Things like 'never use Docker locally', 'always write tests first', 'ask before pushing to remote'. Say 'none' to skip."

If the user provides rules, store each as category: `rule` with the user's reasoning if given. If they say none, skip.

**Question 5 — Current project:**
> "What are you working on right now? (project name, goal, where you are with it)"

Store as category: `project` with temporal anchor: "As of YYYY-MM-DD, ..."

### Instant Recall Demo

After all questions are answered, **immediately demonstrate the value** by generating a mini-briefing. Call `memory_search` with "identity preferences rules technical project" to retrieve what was just stored, then present:

> **Here's what any new session will know about you from now on:**
>
> [2-3 sentence natural language summary synthesized from the stored memories. Not a list — a paragraph that reads like a colleague's mental model of the user.]
>
> **[N] memories stored.** These persist across every session and agent. Run `/mem0-memory review` anytime to update them.

This is the critical moment — the user sees the payoff of onboarding. Make the summary feel personal and useful, not robotic.

### Storage Rules

- Third person: "User is Sarah, senior backend engineer at Stripe" — not "I am Sarah"
- 15-50 words per fact
- Group related info about the same entity into one fact (don't fragment)
- Never store credentials or secrets — if they mention API keys, store that the key was configured, not the value
- Use specific names, never pronouns
- Preserve the user's own words for opinions and preferences

---

## 2. Review

Goal: Let the user audit, correct, and clean up their stored memories interactively.

### Process

**Step 1 — Load and display:**
Call `memory_list` to retrieve all stored memories. Present them grouped by category in this order: `identity`, `rule`, `configuration`, `preference`, `decision`, `technical`, `relationship`, `project`.

Format:
```
### Identity (2 memories)
1. [mem-abc1] User is Sarah, senior backend engineer at Stripe
2. [mem-d4e2] User is based in PST timezone, prefers async communication

### Rules (1 memory)
3. [mem-f7g3] User rule: always write tests before implementation. Reason: caught a prod regression that tests would have prevented

### Technical (1 memory)
4. [mem-h8i4] User's stack: Python/FastAPI backend, Next.js frontend, PostgreSQL, deployed on AWS EKS
```

Show the first 8 characters of the memory ID in brackets. Number memories sequentially across categories for easy reference.

**Step 2 — Interactive editing:**
> "Want to correct, delete, or add anything? Examples:
> - 'Delete #3'
> - 'Update #1 — I'm now at Google'
> - 'Add: I prefer dark mode in all tools'
> - 'Looks good' — done"

**Step 3 — Execute and loop:**
- **Delete**: `memory_delete` with the memory ID
- **Update**: `memory_update` with the memory ID and corrected text (maintain third person, 15-50 words)
- **Add**: `memory_add` with the new fact in the appropriate category

Continue the loop until the user says they're done. Then:

> "Review complete. **[N] memories** — [added] added, [updated] updated, [deleted] deleted."

---

## 3. Export

Goal: Export all memories to structured markdown for backup, sharing, or portability.

### Process

**Step 1:** Call `memory_list` to retrieve all stored memories.

**Step 2:** Generate a markdown document:

```markdown
# Mem0 Memory Export
> Exported on YYYY-MM-DD | Total: [N] memories

## Identity
- [each identity fact]

## Rules
- [each rule fact]

## Configuration
- [each config fact]

## Preferences
- [each preference fact]

## Decisions
- [each decision fact]

## Technical
- [each technical fact]

## Relationships
- [each relationship fact]

## Projects
- [each project fact]
```

Skip empty categories. Include the temporal anchors as-is.

**Step 3:** Present in a code block for easy copying, then offer to save:

> "Here's your full memory export ([N] memories). Want me to save it to `./mem0-export-YYYY-MM-DD.md`?"

---

## 4. Handoff

Goal: Generate a concise, human-readable briefing that gives a new agent or session full context about this user — as if a colleague is handing over.

### Process

**Step 1:** Call `memory_list` to get all memories.

**Step 2:** Call `memory_search` with queries "identity role background", "preferences communication style", and "current projects goals" to get relevance-ranked results.

**Step 3:** Synthesize into a briefing document. Write this as **natural prose**, not just a list dump. Each section should read like a sentence or short paragraph that a human colleague would write:

```markdown
# Agent Briefing — [User Name]
> Generated on YYYY-MM-DD from [N] stored memories

## Who they are
[2-3 sentences: name, role, company, location/timezone. Written as natural prose.]

## How to work with them
[1-2 sentences synthesizing communication preferences and standing rules. Focus on what matters for a productive interaction.]

## Technical context
[1-2 sentences on their stack, tools, and development environment.]

## What they're working on
[Bulleted list of active projects with status, deadlines, and key context. Include temporal anchors.]

## Key people and relationships
[Bulleted list of people/teams mentioned, with their roles and relevance.]

## Important decisions and lessons
[Bulleted list of decisions with rationale — these represent hard-won context that shouldn't be re-debated.]
```

Skip sections that have no memories to draw from. Never fabricate content.

**Step 4:** Present the briefing, then offer to save:

> "Here's the handoff briefing. A new agent reading this will have the context it needs from day one. Want me to save it to `./mem0-briefing-YYYY-MM-DD.md`?"

---

## Tool Reference

| Tool | Used in | Purpose |
|------|---------|---------|
| `memory_add` | Onboard, Review | Store new facts |
| `memory_list` | Smart Entry, Review, Export, Handoff | Load all memories |
| `memory_search` | Onboard (recall demo), Handoff | Relevance-ranked retrieval |
| `memory_update` | Review | Correct existing facts |
| `memory_delete` | Review | Remove facts |

All tools are provided by the **openclaw-mem0** plugin.
