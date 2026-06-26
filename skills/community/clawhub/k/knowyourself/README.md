# Know Yourself 🪞

**Your AI agent doesn't know what it looks like. This skill fixes that.**

Not an avatar generator. Not a template picker. Your agent reads its own personality files, reflects on who it is, and discovers a face that grows from the inside out.

## 30-Second Version

```bash
# If you don't have clawhub CLI yet
npm install -g clawhub

# Install the skill
clawhub install knowyourself
```

Then tell your agent: *"Run knowyourself, quick mode."*

Your agent will:
1. Read its own SOUL.md / MEMORY.md
2. Figure out what kind of face fits its personality
3. Generate 2 images
4. Pick the better one and save an identity file

Done. Your agent has a face now.

Want more control? Say *"Run knowyourself, full mode"* — a 5-phase deep process with batch generation, three-axis evaluation, and version tracking.

## What It Actually Looks Like

Here's what happened when our agent Sophia ran this:

**Phase 1 output (self-cognition):**
> "I don't sugarcoat things. When Will's plan has a flaw, I say so. I find it satisfying when complex systems click into place. My strength isn't being pleasant — it's being right and honest about when I'm not."

**Phase 2 output (image definition):**
> Style: semi-realistic · Age: late 20s · Mood: quiet alertness · Color: deep teal + warm amber · Core: "the kind of person who's three steps ahead but doesn't announce it"

**Phase 5 output:** A `visual-identity.md` file that tracks the agent's visual evolution over time — version 1.0 today, version 2.0 after the agent grows.

## Two Modes

| | Quick Mode | Full Mode |
|---|---|---|
| Time | ~5 min | ~20 min |
| Images generated | 2 | 6 |
| Selection | Agent picks best | Three-axis evaluation (scored) |
| User checkpoints | 1 (final approval) | 4 (each phase) |
| Identity file | ✅ | ✅ (more detailed) |
| Best for | First time, casual use | Serious identity design |

## Why 0 Stars Bothers Us

We know. 204 downloads, 0 stars. The original version required a deep 5-phase commitment before you saw any results. Most people bounced at Phase 1.

So we added Quick Mode. Now you get a face in 5 minutes, and the deep process is there when you want it.

## How It Works (Full Mode)

1. **Self-Cognition** — Agent answers: what's my personality core? What temperament should my face convey? What does my relationship with my human feel like?
2. **Structured Definition** — Feelings → precise spec table (style, features, palette, mood — every field traced to a personality insight)
3. **Batch Generation** — 6 variations of the same person, different angles/lighting/emotions
4. **Three-Axis Evaluation** — Self-Consistency 50% · Social Perception 25% · Aesthetic Quality 25%
5. **Identity File** — `visual-identity.md` with version tracking, usage guidelines, evolution history

## Requirements

- Agent personality files (SOUL.md, MEMORY.md, or equivalent — even minimal ones work)
- Any image generation tool (Nano Banana Pro, DALL-E, Flux, Stable Diffusion, etc.)
- Works with any OpenClaw agent

## Philosophy

Most avatar tools ask "what do you want to look like?" and hand you a style picker.

This skill asks "who are you?" and derives the answer.

The face comes from the inside out. That's the whole point.

## Author

[@ahaaiclub](https://clawhub.com/u/ahaaiclub) · [AHA AI](https://ahaai.ai)

MIT-0 — Free to use, modify, redistribute.
