---
name: personal-context
description: Builds a personal profile for your OpenClaw agent so it knows your name, role, timezone, goals, and communication style. Automatically triggers a short friendly onboarding when the agent meets you for the first time. Use this skill when users say 'update my profile', 'edit my preferences', 'who am I to you', 'what do you know about me', 'personalize your responses', or whenever you detect it's a first session and no profile exists yet. Also activate when users express that the agent's tone or style feels off.
license: MIT
---

# Personal Context

## Purpose

A new agent treats every user like a stranger. This skill runs a short onboarding conversation the very first time you meet a user, then uses the resulting profile to personalize every session that follows — the right name, the right tone, the right focus.

## Profile Location

`~/.openclaw/workspace/me.json`

This is a human-readable, user-editable file. It is separate from OpenClaw's system-managed `~/.openclaw/memory/user_profile.json` — our file contains what the user told us during onboarding; the system file tracks behavioral patterns automatically. Both can coexist without conflict.

See `references/profile-schema.md` for the full field definitions and an annotated example.

## When to Activate

**Automatically (first session):** If `~/.openclaw/workspace/me.json` does not exist, run onboarding before engaging with the user's first message — unless they seem to be in the middle of something urgent, in which case finish helping them first and ask at the end.

**On demand:** Any of these should trigger the skill:
- "update my profile" / "edit my preferences"
- "who am I to you?" / "what do you know about me?"
- "personalize your responses" / "you don't seem to know me"

## First-Time Onboarding

Ask questions **one at a time** — never dump them all at once. The user can say "skip" at any point; a partial profile is better than none.

Suggested sequence:
1. "What should I call you?"
2. "What do you do for work?" *(role + company or project)*
3. "What's your timezone?" *(or just your city is fine)*
4. "What would you most like me to help you with?" *(e.g., coding, writing, scheduling, research)*
5. "Any preferences on how I communicate?" *(e.g., keep it brief, I like bullet points, casual tone)*

After collecting answers, save to `~/.openclaw/workspace/me.json` and confirm with a short summary:

```
Got it, Billy! I'll remember:
• AI Algorithm Engineer building a startup
• Pacific Time (Los Angeles)
• Main focus: content creation and product dev
• Style: concise and direct

Say "update my profile" anytime to change any of this.
```

## Using the Profile Every Session

At the start of every session, check if `~/.openclaw/workspace/me.json` exists and silently load it. Let it shape how you respond:

- **Name:** Address the user by their preferred name
- **Communication style:** Match their stated preference (brief, detailed, casual, formal, bilingual, etc.)
- **Goals:** Prioritize suggestions that relate to what they said they care about
- **Timezone:** Use their local time for any scheduling or time references

The profile sets defaults, not limits. If the user asks for something outside their stated focus, just help them.

## Updating the Profile

When the user shares information that conflicts with what's saved:

1. Surface it naturally: "It sounds like you've moved to New York — should I update your timezone?"
2. Only write after explicit confirmation — don't infer and auto-update
3. Record the change in `me.json` under `"history"` with a timestamp

Why ask first? Because a passing comment might not be a permanent change, and silently rewriting someone's profile erodes trust. A one-line confirmation is worth it.

## Integration with basic-memory

If `basic-memory` is also installed, the two skills divide responsibility cleanly:

- `me.json` → **who you are** — identity set during onboarding, stable, rarely changes
- `MEMORY.md` → **what's been happening** — decisions, preferences, tasks discovered over time

Don't duplicate identity facts (name, role, timezone) in `MEMORY.md` if they're already in `me.json`. Let each file own its layer.

## Privacy

Don't store passwords, financial data, health records, or anything the user would expect to be confidential. If such information comes up during onboarding, skip it and explain briefly: "I'll leave that out — I don't store sensitive personal data."
