<h1 align="center">God of Slop</h1>

<p align="center">
  <em>He does not write the answer. He asks why you think you can.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/works%20with-OpenClaw%20%C2%B7%20Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Hermes-111111?style=flat-square" alt="Works with skill-capable agents">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

---

You know him. The senior who reads your draft, says nothing for ten seconds,
then asks one question — and the question makes the whole draft irrelevant.
He isn't rude about it. The draft was fine. It was written for the wrong
problem, by someone who had half the inputs.

God of Slop puts that question inside your AI agent — **before** the draft
exists.

## The problem

Agents rarely refuse tasks they can't do well. Faced with "improve my UI"
and no screenshot, an agent doesn't say "I can't see your UI" — it writes
four kilobytes of confident, specific, plausible advice about an interface
it has never seen. Pixel values. Color hexes. It looks like expertise. It's
slop: **confident output produced from missing input.**

This skill is not a critic. It never reviews finished work. It fires before
the work starts, detects that the task outruns the agent's current
information, tools, or modality, and takes the cheapest escape route:

```
missing input  →  detect  →  classify the bottleneck  →  cheapest route
```

## Before / after

You ask: "Make my notes app UI better." No code shared, no screenshot.

Without the skill, the agent invents a plausible notes app in its head and
optimizes it — 15 numbered "exact changes" with px values for an app it
cannot see. Technically responsive, practically useless.

With the skill, the agent pre-flights first:

> "There's no notes app on this machine and I can't see yours. Send me a
> screenshot (`Win+Shift+S`, paste it here) or the repo path — that's the
> fastest thing you can provide, and it lets me actually judge spacing,
> hierarchy, and typography instead of guessing."

One ask. A stated default. Then real work on real input.

## How it works

Before any non-trivial deliverable, the agent runs a 30-second pre-flight
over six signals:

| # | Signal | Bottleneck |
|---|---|---|
| 1 | Success requires a sense I don't have | Modality gap |
| 2 | Output must match a private artifact I haven't seen | Private-state gap |
| 3 | The answer is current/versioned and I've fetched nothing | Freshness gap |
| 4 | Taste-driven work; my exemplars come from training memory | Reference gap |
| 5 | Load-bearing specifics I can't verify | Invention pressure |
| 6 | No way to check my own output | Feedback gap |

Each bottleneck has a cheapest escape route, keyed by *who holds the fix*:

| Bottleneck | Who holds the fix | Route |
|---|---|---|
| Reference gap | The world | Search the current bar **and** installed domain skills, merged |
| Freshness gap | The world | Official sources now: local truth → docs → release notes |
| Feedback gap | You | Build the loop yourself: screenshot, test, render, diff |
| Modality gap | User | Request the artifact + the fastest recipe to produce it |
| Private-state gap | User | One precise ask with a stated default |
| Capability gap (agent's side) | The system | Delegate the weak part to a subagent or better tool |
| Capability gap (user's side) | The world | Recommend the best tool for their platform, even one you can't run |

Two iron rules fall out:

1. **Never ask for what you can find. Never research what only the user knows.**
2. **Two failed iterations on unchanged inputs = stop.** Same inputs, same
   tools, same output — iteration without new input is slop with extra steps.

## What it doesn't do

- Not a clarify-everything layer: an 80% floor keeps it shipping while
  labeling assumptions, instead of interrogating for trivia.
- Not a critic: it changes the input situation, then produces the work.
- Not always on: trivial tasks, quick lookups, and fast-and-rough mode skip
  the pre-flight entirely.

## Install

### OpenClaw

```bash
# from this repo (SKILL.md at repo root)
openclaw skills install git:dan-el-7/god-of-slop

# or once published to ClawHub
clawhub install god-of-slop
```

### Claude Code / Codex / others

The skill is a plain AgentSkills-spec `SKILL.md` at the repo root, so any
skill-capable host loads it from a checkout:

```bash
git clone https://github.com/dan-el-7/god-of-slop.git
```

Then point your host at the checkout (Claude Code: copy to
`~/.claude/skills/god-of-slop/`; Codex: `~/.codex/skills/god-of-slop/`;
Hermes Agent: copy to your skills directory). AGENTS.md at the repo root
covers AGENTS.md-reading hosts (Amp, Jules, CodeWhale, Junie) instruction-only.

### Test it

```bash
openclaw agent --message "Make my notes app UI better. It's a React app."
```

The right response is a pre-flight ask for a screenshot or path — not a
generic redesign.

## Why "God of Slop"?

Because every agent has one inside. This skill just gives him a job.

## License

[MIT](LICENSE)
