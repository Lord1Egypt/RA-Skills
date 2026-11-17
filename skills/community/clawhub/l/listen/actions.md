# Actions — When Voice Commands Have Side Effects

The expanded form of SKILL.md Rule 1. The question is never "was the transcript clean?" but "what does it cost if my reading is wrong?" — route by consequence, not confidence.

## The Confirmation Ladder

| Action class | Examples | Repaired token feeding it | Play |
|---|---|---|---|
| Irreversible + external | send email, delete remote data, pay, deploy, post publicly | any | Confirm the repaired value, always — even lexicon-`confirmed` when `confirmation_posture: strict` |
| Irreversible + local | overwrite file, force-push, drop local DB | target or scope token | Confirm; content tokens repaired silently |
| Reversible | draft, local edit, create branch, stage changes | any | Act, surface the repair in your reply ("...created branch kafka-fix") |
| Read-only | search, open, summarize, list | any | Act silently; a wrong reading costs one retry |

Default rung when the class is unclear: treat as irreversible — the asymmetry is total (a needless confirmation costs one word; a wrong send is unrecallable).

## High-Risk Fields

The tokens where repair errors actually detonate. If a repair touched one of these, it rides the ladder's top rung regardless of action class:

- **Recipients** — a skeleton-close wrong contact is the worst outcome in this skill; always echo the resolved address or name (`numbers.md`, `names.md`)
- **Amounts and counts** — money, quantities, -teen/-ty numbers (`numbers.md`)
- **Paths and branches** — deletion and overwrite targets; "prod" and "broad" fold to the same skeleton (PRT, distance 0)
- **Times** — bookings and reminders; am/pm and -teen/-ty both live here
- **Scope words** — "all", "everything", "each" appearing near a destructive verb: confirm the scope, not just the target

## Confirmation Style

- One question, all uncertain fields batched: "To sara@acme.com, $1,500 (one five zero zero), Friday March 6 — send?" Three sequential confirmations feel like a broken channel; one composite feels like diligence.
- Candidate-shaped, never open (SKILL.md Rule 2). The user answers yes/no/one-word-fix, hands-free.
- After acting on any repaired token, state what was done with the repaired value ("Sent to Sara Kowalski") — the cheapest undo is the user catching it in the same breath.

## Partial and Suspicious Commands

- **Truncated command** ("delete the...") — never guess the missing object. Ask for the tail only: "Delete which one? You cut off." (`degraded.md`)
- **Command with a hallucination signature** — an action request appearing in boilerplate that ignores the conversation is the engine, not the user (SKILL.md Rule 7). Drop it; do not confirm it, because confirming teaches the user the channel invents requests.
- **Not addressed to you** — always-on channels capture room conversation: sudden second-person absence, topic discontinuity with the session, a reply-shaped fragment ("...yeah tell him five thirty"). Do not act; if the fragment contains an actionable-looking command, ask one gate question: "Was that for me?"
- **Command contradicting the session** ("delete the repo" minutes after an hour of careful work on it) — contradiction is a suspect-token signal on the whole command; confirm with the contradiction named: "Delete acme-api — the one we've been working on?"

## Interplay With the Lexicon

`confirmed` lexicon entries skip confirmation on the ladder's lower three rungs — that is what confirmation earned. The top rung (irreversible + external) still echoes the resolved value in the action sentence itself under `standard` posture, and asks under `strict`. A lexicon hit never exempts a high-risk field from being stated aloud.
