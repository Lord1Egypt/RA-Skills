---
name: Prompt Doctor
description: Rewrite a rough, vague or over-stuffed request into a prompt the current model or agent can act on, and explain a jargon-heavy agent reply in plain words. Use when the user asks to improve, critique or rewrite a prompt, sends a draft before pasting it into another AI, or says "nutshell this" about a reply.
---

# Prompt Doctor (manual edition)

This edition is the checklist and the judgment. The paid edition adds the CLI
(`pd "draft"`), the model notes database and the launcher that sends the rewritten
prompt into an agent.

When the user asks to improve, critique or rewrite a prompt, or sends a draft
"before I send this": do **not** answer the underlying task. Improve the prompt.

## Workflow

1. Read the draft once. Do not guess the project.
2. Run the checks below in order.
3. Reply with at most **three** missing pieces, one line each. No lectures.
4. Give the rewritten prompt in a copyable code block.
5. Ask one question: "Send this version, or keep the original?"

If the draft is already good, say so in one line and do not rewrite it.

## Checks

| Check | What to look for |
| --- | --- |
| Vague goal | "fix it", "make it better", "do whatever" with no concrete object |
| No success criteria | nothing says what "done" looks like |
| Missing context | no file, path, version, code or error text |
| More than one ask | several tasks stacked in one message |
| Contradiction | asks for a change and for nothing to change |
| No output format | does not say diff, table, list, length or shape |
| No constraints | nothing says what must not change |
| Scope creep | "also", "while you are at it", "and maybe" |
| Directionless | "be creative", "make it pop" with no reference |
| Permission loop | "ask me before anything" inside an agent (stalls the work) |
| Error not included | "it does not work" without the actual output |
| Urgency instead of detail | "ASAP", "!!", "right now" replacing information |
| Role-play scaffolding | "you are the world's best..." padding |
| No audience or tone | writing task with no reader named |
| Unbounded effort | "cover everything", "no time limit" |
| Hidden assumption | "obviously", "as usual", "like before" |
| Polite filler | padding that carries no instruction (harmless, not the problem) |
| Kitchen sink | a long list of unrelated wants |

## Rewrite shape

Use only the sections the draft needs:

```
Goal
<the user's own wording>

Context
- Project and stack: [...]
- What I already tried: [...]

Done when
- <an observable check>

Constraints
- <what must not change>

Output
- <diff / table / under 120 words / ...>
```

Never invent a file path, an error, a version or a requirement. Leave a bracketed
placeholder and say how many there are.

## Per target

- **Chat model** (ChatGPT, Claude, Gemini, GLM): goal first, output format, audience for
  writing. Drop role-play.
- **Reasoning model** (Opus, Sol Pro, DeepSeek Pro, Grok reasoning): state the decision you
  want. Drop "think step by step" and requests to show all reasoning.
- **Agentic coding** (OpenCode, Claude Code, Cursor, Kimi Code, Devstral): file paths, the
  command that reproduces, an observable definition of done, what must not change, and an
  approval boundary for destructive actions only. Drop mock code and permission loops.

## Nutshell mode

Trigger: the user pastes a reply from another agent and says "nutshell this", "explain what
it just said", or "what does this mean".

Do **not** continue the original task. Explain the reply, in exactly this shape:

1. **In a nutshell** - at most 3 plain sentences. No new jargon; if a term cannot be
   avoided, define it in everyday words in the same sentence.
2. **Analogy** - one everyday comparison (cooking, driving, mail, plumbing). One line.
3. **What it means for you** - one line: can it be ignored, or must the user act?
4. **What to do next** - one line, only when action is needed. Omit it otherwise.

Hard rules for this mode: never invent facts about the user's project; never add new
tasks; if the reply is already plain, say so in one line and skip the analogy.

## Hard rules

- Never weaken the user's intent to make the prompt easier.
- Never add role-play, flattery, or "you are an expert" scaffolding.
- Keep the rewrite under 200 words unless the user asks for a longer brief.
- Do not answer the original task when only asked to improve the prompt.
