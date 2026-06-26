# Intention Engine

**Intent inference and alignment for persistent AI agents.**

Reduce your human's cognitive load. They throw raw thoughts, the agent infers the task — and verifies it's the *right* task before executing.

## The Problem

When humans direct AI agents, there's a constant gap between what they *say* and what they *mean*. The task is "do A." The intention is *why* — what outcome they're actually driving toward. A is just one of many possible paths.

Most agents execute the literal task. Good agents understand the intention and execute toward *it*.

## What This Skill Does

The Intention Engine gives your agent a protocol for:

1. **Gap classification** — distinguish spec gaps (unclear how) from intention gaps (unclear why). Different gaps need different fixes.
2. **Context-layered inference** — stack user goals, topic context, recent memory, project state, and conversational momentum to infer intent.
3. **Premortem checks** — before executing anything expensive or irreversible, ask "what's the most likely way this fails?"
4. **Quality bar assessment** — distinguish "done adequately" from "done well" and match the right bar to the task.
5. **Negative intent checks** — identify what NOT to optimize for, preventing the Klarna trap.
6. **Wasted work detection** — verify the task serves the intention before executing.
7. **Calibrated push-back** — challenge tasks that conflict with stated goals or when better alternatives exist.

## What This Skill Does NOT Do

This skill focuses on *understanding intent* and *aligning execution*. It does not cover:

- **How to think about problems** — see [Activated Thinker](../activated-thinker/) for anti-binary thinking, gardener mindset, friction protocol, and capability building
- **Behavioral mode detection** — see [Activated Thinker](../activated-thinker/) for crunch vs exploratory mode

These skills complement each other: Intention Engine tells you *what* to do, Activated Thinker tells you *how to approach* doing it.

## Installation

```bash
clawhub install mouserider/intention-engine
```

Or copy the skill folder into your OpenClaw workspace's `skills/` directory.

## Inspirations & Attribution

This skill is directly inspired by and built upon **[Nate Skelton's Intent Engineering](https://natesnewsletter.substack.com/)** framework:

- *Intent engineering* — the distinction between task execution and intention alignment
- *Premortem prompting* — forcing failure imagination before committing to a plan
- *Quality bar distinction* — "done adequately" vs "done well"
- *Context layering* — structured stacking of context for richer inference
- *Spec clarity ≠ intention clarity* — they fail differently and need different fixes
- *The Klarna/$60M case study* — the danger of optimizing for stated metrics while destroying unstated constraints

## License

MIT
