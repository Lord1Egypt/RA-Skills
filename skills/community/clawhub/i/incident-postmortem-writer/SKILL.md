---
name: incident-postmortem-writer
version: 1.0.0
description: Structure a blameless incident postmortem from rough notes: timeline, impact, root cause, and follow-ups with owners. Use after any outage, security event, failed automation or costly mistake.
---

# Incident Postmortem Writer

## Overview

Converts scattered notes, logs and memories of an incident into a postmortem that actually prevents recurrence: a verified timeline, an honest impact statement, a root cause that goes past the first explanation, and follow-ups with owners and dates.

## When to use

Within a few days of any incident, while evidence is still available.

## Workflow

1. **Collect raw material** — logs, timestamps, messages, what people remember; keep facts and interpretations in separate piles
2. **Build the timeline** — every entry timestamped from a source, not from memory; mark gaps explicitly
3. **State the impact** — who/what was affected, for how long, and how it was detected (and how long detection took)
4. **Find the root cause** — ask 'why' until the answer is a system property, not a person's error
5. **List contributing factors** — the conditions that let one mistake become an incident
6. **Write follow-ups** — each with one owner, one concrete change, and a date; 'be more careful' is not a follow-up
7. **Close with what went well** — the responses worth repeating

## Guardrails

- Blameless means describing actions and systems, never character
- Never invent timestamps or details to make the timeline look complete — mark unknowns as unknowns
- Do not soften impact numbers; the reader must be able to trust every figure

## Output format

A postmortem document: summary, impact, timeline, root cause, contributing factors, follow-ups (owner + date), what went well.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
