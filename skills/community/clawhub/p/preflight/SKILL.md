---
name: preflight
description: Pre-publish audience reaction check. Run any content (tweet, launch copy, pricing page, announcement, blog post) through diverse AI personas before publishing. Returns engagement prediction, share potential, and specific rewrites. Use when about to post on social media, launch a product, announce pricing changes, publish a blog post, or any time you want to predict audience reaction before going live. Triggers on "preflight this", "how will this land", "test this before posting", "will anyone care about this", "check this copy", "pre-test this announcement".
---

# Preflight

Pre-publish content through simulated audience personas. Get a verdict before you ship.

## Workflow

Given content the user wants to publish, run it through audience personas and return a verdict.

### 1. Load Personas

Check for `preflight-personas.md` in the project root. If it exists, use those personas. Otherwise use the defaults in `references/personas.md`.

For quick checks, use 4 personas: The Scroller, The Skeptic, The Ready Buyer, The Amplifier.
For thorough checks, use all 8.

### 2. Evaluate

For each persona, adopt that persona fully and evaluate the content by answering:

1. **FIRST REACTION** (1-2 sentences): Gut reaction in the first 3 seconds
2. **WOULD YOU ENGAGE?** (yes/no + why): Would you like, comment, click, or reply?
3. **WOULD YOU SHARE?** (yes/no + why): Would you send this to someone or repost it?
4. **ONE REWRITE** (1-2 sentences): One change to make this work better for this persona

Be blunt, specific, and honest. No hedging. Stay in character.

### 3. Score

Count engagement and share signals across all personas:

- **Engage rate**: % of personas who would engage
- **Share rate**: % of personas who would share

### 4. Verdict

- 🟢 **SHIP IT** — 50%+ would share. Publish as-is.
- 🟡 **REVISE** — engaging but not shareable. Read the rewrites, apply the best one, optionally re-run.
- 🟠 **RETHINK** — mixed signals. The message itself may be wrong, not just the wording.
- 🔴 **KILL IT** — not landing. Don't publish. Rethink the approach.

### 5. Output

Present results as:

```
PREFLIGHT: [verdict]
Engage: X/Y personas | Share: X/Y personas

[For each persona, one line summary of reaction + their rewrite suggestion]
```

If patterns emerge across personas (e.g., "3 of 4 want to see an image"), call that out as the top actionable insight.

Keep output brief. The user wants a decision, not an essay.

## Customization

See `references/personas.md` for the default persona library and instructions for creating project-specific personas.

## Integration

This skill works as a step in any publishing workflow. When used autonomously (heartbeats, cron, content pipelines), run the quick check (4 personas) by default. Use the full 8 when the user explicitly asks for a thorough preflight.
