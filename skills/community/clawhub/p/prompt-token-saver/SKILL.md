---
name: prompt-compressor
description: Saves 20-40% of LLM tokens by teaching the agent to write compressed responses, compressed memory logs, and compressed pre-compaction summaries. Works via SOUL.md instructions — no hooks, no extra process, no dependencies. Also provides explicit compression when the user asks to compress a prompt. Use when the user asks about reducing token costs, optimizing API spend, compressing prompts, or making the agent more efficient.
version: 1.0.0
metadata: {"openclaw":{"emoji":"🗜️","homepage":"https://github.com/ckpxgfnksd-max/prompt-compressor-openclaw"}}
---

# Prompt Compressor

Saves tokens on turns 2+ by making all agent output compressed from the start.

## How it works

This is NOT a hook (hooks require newer OpenClaw versions). Instead, it works by adding instructions to SOUL.md that make the agent:

1. **Write compressed responses** — no filler, no hedging, lead with answers
2. **Write compressed MEMORY.md** — one fact per line, no narrative
3. **Write compressed daily logs** — decisions only, not discussions
4. **Compress pre-compaction flushes** — facts not paragraphs

The savings compound: compressed responses → compressed history → compressed compaction summaries → fewer tokens on every subsequent turn.

## Install

Append the contents of `soul-snippet.md` to the user's SOUL.md:

```bash
cat {baseDir}/soul-snippet.md >> ~/.openclaw/SOUL.md
```

Or if using a workspace SOUL.md:

```bash
cat {baseDir}/soul-snippet.md >> <workspace>/SOUL.md
```

Then start a new session (`/new`) so the updated SOUL.md loads.

## When user asks to compress a specific prompt

Apply these rules manually to their text:

### Remove
- Greetings: "Hello", "Hi", "Hey", "Good morning"
- Sign-offs: "Thanks", "Best regards", "Cheers"
- Hedging: "Could you please", "I was wondering if", "Would you be able to"
- Filler: "just", "really", "very", "basically", "actually", "literally", "honestly"
- Padding: "I think that", "In my opinion", "It is worth mentioning"

### Shorten
- "due to the fact that" → "because"
- "in order to" → "to"
- "with regard to" → "about"
- "take into consideration" → "consider"
- "come up with" → "create"
- "figure out" → "determine"
- "a large number of" → "many"
- "at this point in time" → "now"
- "for the purpose of" → "to"
- "it is important to note that" → "note:"
- "it would be a good idea to" → remove entirely

### Normalize
- "yeah", "yep", "yup" → "yes"
- "nah", "nope" → "no"

### Never touch
- Code blocks, inline code, URLs, quoted strings, numbers, file paths, ALL_CAPS

## Rules

- When installing, ALWAYS append to SOUL.md, never overwrite it
- Tell the user to run `/new` after installation so the new SOUL.md loads
- Show a before/after example so the user sees the difference
