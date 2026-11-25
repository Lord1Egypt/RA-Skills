# Prompt Doctor — make a rough prompt one the model can act on

Free agent skill. Paste a draft, get the missing pieces named and a rewritten prompt you
can send.

You know the pattern: you type "fix the login on mobile", the agent guesses, edits five
files, and calls it done. The prompt was the problem, not the model.

This skill turns your agent into a prompt reviewer. It does not answer the task — it
fixes the ask first.

## What it does

1. Reads your draft once and refuses to guess your project.
2. Runs 18 checks in order: vague goal, no success criteria, missing context, more than
   one ask, contradictions, no output format, no constraints, scope creep, directionless
   requests, permission loops, missing error text, urgency without detail, role-play
   padding, missing audience, unbounded effort, hidden assumptions, filler, kitchen sink.
3. Names at most **three** missing pieces, one line each.
4. Returns the rewritten prompt in a copyable block, using only the sections the draft
   needs: `Goal`, `Context`, `Done when`, `Constraints`, `Output`.
5. Asks one question: "Send this version, or keep the original?"

Hard rules baked in: never invent a file path, error, version or requirement; leave a
bracketed placeholder instead; never add role-play or "you are an expert" scaffolding;
never answer the task when only asked to improve the prompt.

It adapts to three targets: **chat** models, **reasoning** models (drop "think step by
step"), and **agentic coding** tools (paths, reproduction command, definition of done,
approval boundary for destructive actions only).

## Install

```
npx skills add WinSoftLabs30/prompt-doctor-skill
```

On ClawHub (OpenClaw): `openclaw skills install @winsoftlabs30/prompt-doctor`, or
`clawhub install @winsoftlabs30/prompt-doctor` with the ClawHub CLI.

Or copy `SKILL.md` into:

- **OpenCode** — `.opencode/skills/prompt-doctor/` in your project, or
  `~/.config/opencode/skills/prompt-doctor/` for every project
- **Claude Code** — `.claude/skills/prompt-doctor/`
- **Other agents** — any that read the `SKILL.md` format (Cursor, Gemini CLI, ...)

OpenChamber runs on OpenCode, so the OpenCode path works there too.

No build step, no dependencies, no API key. Any Node version works for this manual
edition.

## Use

Send your agent a draft, or ask:

- "improve this prompt before I send it"
- "why is this prompt bad?"
- "rewrite this so the agent stops guessing"

The skill loads and follows the workflow. It works on any draft, not just coding ones —
emails, briefs, research questions, agent instructions.

## Nutshell mode

Paste an agent's reply and say **"nutshell this"**. The skill stops working on the task and
explains the reply in at most 3 plain sentences, adds one everyday analogy, says in one
line whether you must act, and one line on what to do next if so. No new jargon, no new
tasks, no invented facts.

## Try it without installing

Paste this into a ChatGPT Project, Claude Project or Gemini Gem once, and it reviews
every draft you send after that:

```
Before you answer any request I send, check it for: a concrete goal, success criteria,
context, one task, contradictions, output format, constraints, scope creep, direction,
permission loops, the actual error, urgency without detail, role-play padding, audience,
effort bounds, hidden assumptions, filler, kitchen sink.

If two or more fail: list the missing pieces (max 3, one line each), give me a rewritten
prompt in a code block, then ask "Send the rewritten prompt, or answer the original?".
If nothing important fails, answer normally. Never invent details about my project.

When I paste an agent's reply and say "nutshell": explain it in at most 3 plain sentences,
no new jargon, add one everyday analogy, and say in one line whether I need to act.
```

## Manual edition

This repository is the checklist and the judgment. The paid edition adds the CLI
(`pd "draft"` — score 0-100, issues by severity, rewritten prompt, `--json`, `--copy`),
the verified per-model notes database, and the launcher that hands the rewritten prompt
straight to OpenCode or Claude Code.

## Honest limits

- Rules, not a model. It catches structure, not meaning: a well-structured prompt about
  the wrong thing still passes.
- It cannot see your repository or your conversation history. You still supply the facts
  it leaves in brackets.
- Adding detail is on you. The skill names what is missing; it never invents the missing
  fact.

## License

MIT-0 — see [LICENSE](LICENSE). Use it, modify it, redistribute it, no attribution
needed. (ClawHub requires MIT-0, so both free channels use one license.)
