# handover-sync

中文说明: [README.md](./README.md)

`handover-sync` is a documentation-sync skill for the end of a development session. Its job is not to generate a vague recap. Its job is to turn actual repository evidence into a handoff another engineer or agent can pick up immediately.

This repository is useful if you want a repeatable way to:

- summarize real work done in a session
- sync `handover.md`, `README.md`, and nearby run notes together
- capture problems, fixes, validation, and next steps before stopping
- preserve enough context that the next person does not need to reread the full conversation

## What It Does

The skill inspects the repo first, then writes a grounded handoff based on what actually changed.

It is designed to answer three practical questions:

1. What changed?
2. What is still risky, broken, or unfinished?
3. What should the next person do first?

This is a documentation workflow, not a chat summary workflow.

## Why It Exists

Most end-of-session summaries are too weak to be useful. They often say things like "fixed a few bugs" or "made progress on docs" without naming files, runtime behavior, validation, or remaining risk.

`handover-sync` enforces a higher bar:

- inspect the repo before writing
- name files, commands, behaviors, and validations
- separate verified facts from current judgment
- mark temporary workarounds clearly
- leave the next person with a concrete restart path

## Default Workflow

The skill's normal flow is:

1. Identify the repo root and the effective summary date.
2. Inspect existing handoff targets such as `handover.md` and `README.md`.
3. Load the matching session-summary template.
4. Gather repo evidence from git status, diffs, logs, and changed files.
5. Derive the handoff narrative from observable facts.
6. Update the handoff docs together by default.
7. Read the updated docs back and verify that they are actionable.

## Default Output Scope

Unless the user explicitly narrows scope, the skill updates all of:

- `handover.md`
- README sections made stale by the current session
- nearby TODO notes or run instructions that must stay consistent

If today's conclusions changed the project's current understanding, updating only one file is not enough.

## Expected Handoff Content

A good output from this skill should cover:

- session scope and current objective
- current repo state
- problems actually encountered
- root-cause analysis and conclusions
- implemented fixes
- validation that actually happened
- failed attempts, pitfalls, and constraints
- how to resume work from here
- remaining issues and boundaries
- long-term product direction when relevant
- ordered next TODOs

## Language Behavior

- If the user asks in Chinese, write in Chinese.
- If the user asks in English, write in English.
- If the user explicitly asks for bilingual output, provide both.

When editing an existing document with a strong established language, preserve that language unless the user explicitly asks to switch.

## Repository Layout

- `SKILL.md`
  The formal skill definition, including workflow and writing rules.
- `references/session_summary_template.md`
  Chinese session-summary template.
- `references/session_summary_template.en.md`
  English session-summary template.

## Quick Usage Examples

Use prompts like these:

```text
Summarize today's work and sync the handover plus README.
```

```text
Write down today's problems, fixes, validation, and next steps before we stop.
```

```text
Update the handoff so the next agent can continue without rereading the whole thread.
```

You can also narrow the request:

```text
Summarize changes since the last handover and update only handover.md.
```

```text
Prepare an English handoff for today's changes and sync the README sections that became stale.
```

## What This Skill Is Not For

This skill is not meant to:

- generate a lightweight chat recap
- skip repo inspection and write from memory
- hide unverified work behind generic phrases
- replace real validation with vague confidence

If the repo was not inspected and the output does not name concrete evidence, it is below the bar this skill is intended to enforce.

## Recommended Use

Use this skill whenever you are ending a meaningful work session, not only when context has already become messy.

That keeps `handover.md` and related docs aligned with reality, reduces context loss, and makes handoffs much cheaper for the next engineer or agent.
