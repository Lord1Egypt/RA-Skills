# HOA Nightmare Navigator

**Fight HOA violations, fines, and assessment hikes with procedure instead of anger — due-process letters, fine-cap checks, records demands, and the escalation ladder that makes boards blink.**

## The problem
74 million Americans live in HOA/condo associations. The standard abuse pattern is procedural: a violation letter citing a covenant you've never seen, a fine levied without a hearing, a special assessment "approved" by twelve people at a sparsely-attended meeting, a records request answered with silence. Owners lose these fights while being right, because boards and their attorneys only respond to one language: **which covenant, adopted when, hearing held when, statute says what**. A one-page letter that asks those four questions kills most fines; a 10-year compounding projection beats "this is too much" at open forum.

## What this skill does
- `violation` — due-process response letter demanding covenant text, evidence, hearing, cure period (certified mail ready)
- `fine` — reasonableness check against CA/FL/TX statutory structures (hearingless fines, out-of-band amounts) with defect list and reversal demand
- `assessments` — compounding projection that turns "up 7% again" into a dollar figure and an open-forum statement
- `records` — statutory inspection demand for budgets, minutes, reserve studies, vendor contracts, fine schedules (state-cited)
- Escalation ladder + evidence file template in `references/`

## Quick example
```bash
python3 scripts/hoa_toolkit.py --demo
```
Runs a violation letter, a hearingless-$250-fine review (verdict: FINE IS VULNERABLE), a 10-year assessment projection ($385→$709/mo, +$22k growth premium), and a FL records demand.

## Who needs this
- Any owner under an HOA/COA receiving violation notices or fines
- Owners facing special assessments or runaway dues increases
- Tenant-board coalitions and people considering running for a board seat
- Landlords whose renters get violation letters

## Install
Python 3.9+, stdlib only:

```bash
python3 scripts/hoa_toolkit.py --demo
```

## License
MIT © Denis Voronin
