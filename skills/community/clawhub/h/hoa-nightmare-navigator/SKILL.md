---
name: hoa-nightmare-navigator
description: Use when an HOA or condo association sends a violation notice, levies a fine, denies a records request, hikes assessments, or a neighbor-to-neighbor dispute ends up in front of the board — generates due-process response letters that cite the governing documents, checks fines against state reasonableness caps (CA/TX/FL statutes), projects compounding assessment increases, drafts statutory records-request letters, and lays out the escalation ladder before you ever need a lawyer.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [hoa, condo, homeowners-association, violation, fines, dispute, housing]
---

# HOA Nightmare Navigator

## Overview
74 million Americans live under a homeowners or condo association, and the typical conflict follows the same script: a violation letter with a photo and a deadline, a fine that appears before you can respond, an assessment that climbs faster than inflation, and a board that meets at 6pm on a Tuesday and decides everything before you know a hearing existed. Owners lose these fights not because they're wrong but because they respond emotionally ("this is ridiculous!") instead of procedurally — the only language boards and their attorneys respect is **the covenant cited, the statute it sits under, and the process the association skipped**.

This navigator runs the three plays that actually work:
1. **Violation response** — a dated letter demanding the specific covenant text, notice-and-hearing rights, and evidence, sent before the response deadline. Most fines die here.
2. **Fine reasonableness check** — many states cap or structure fines (CA's schedule-and-heing regime, FL's $1,000 aggregate cap per violation day-structure, TX assessment limits); an out-of-cap fine is leverage.
3. **Records & escalation** — statutory inspection letters, assessment-increase projections that turn a 7%/yr hike into a 10-year dollar figure owners can rally around, and the ladder: internal hearing → board meeting (recorded) → mediation/ADR (often mandatory before litigation) → regulator/AG → small claims.

## When to Use
- A violation notice arrived (landscaping, parking, trash cans, paint, "architectural" issues, fence, holiday decorations)
- A fine was levied, especially without a hearing you were invited to
- Assessments jumped double digits and the annual meeting is coming
- The board ignored or refused a records request (budgets, minutes, contracts, delinquency)
- You're considering running for the board or petitioning for a special meeting

**Don't use for:** construction-defect claims (attorney territory immediately), fair-housing discrimination complaints (file with HUD/state FH agency — different track, cite both anyway if applicable), or municipal code violations (those come from the city, not the HOA, and the response path is different).

## Quick Start
```bash
# Respond to a violation notice with the due-process letter
python3 scripts/hoa_toolkit.py violation --violation "trash cans visible from street" \
    --fine 0 --deadline-days 14 --state CA --ccr "3.7 Trash Receptacles" > response_letter.txt

# Fine arrived without any hearing — check reasonableness and demand reversal
python3 scripts/hoa_toolkit.py fine --fine 250 --violation "fence stain color" \
    --repeat no --hearing-held no --state CA

# What does 7%/yr assessment growth actually cost?
python3 scripts/hoa_toolkit.py assessments --monthly 385 --growth 0.07 --years 10

# Demand the books (budgets, minutes, vendor contracts)
python3 scripts/hoa_toolkit.py records --state CA > records_request.txt

# Full worked demo of every module
python3 scripts/hoa_toolkit.py --demo
```

## Fine Reasonableness Table (verify current statute — these move)
| State | Structure | Typical cap band |
|---|---|---|
| California | Davis-Stirling §5710/§5850: fine schedule must be adopted, hearing before effective date | ~$100 first / escalating; schedule published |
| Florida | Ch. 720 §720.305: 14-day written notice, committee approval (if appointed) | $1,000 aggregate ceiling per violation (condo Ch. 718 similar) |
| Texas | Ch. 209 Prop. Code: assessment limits, notice requirements | fines require notice+opportunity; re-approval limits |
| Most others | Reasonableness doctrine + governing docs | $25–$100/day patterns; must be in adopted schedule |

Out-of-schedule or hearingless fines are the single most reversible HOA action.

## Numbered Workflow
1. **Do not comply-and-fume.** Note the response deadline in the notice (often 14–30 days).
2. Run `violation` — the letter demands: exact covenant text, date/photo provenance, who complained (if required), hearing date, and cure period. Send certified mail + email.
3. If a fine exists, run `fine` — check hearing requirement, cap structure, and generate the reversal demand citing the skipped step.
4. Pull the books with `records` — budgets, reserve studies, minutes, contracts. Follow-the-money turns neighbor disputes into governance disputes (where boards get careful).
5. Run `assessments` before the annual meeting; a 10-year dollar projection beats "this is too much!" at open forum.
6. Escalate in order: written response → open-forum statement (recorded) → internal dispute resolution / mediation (CA requires it pre-litigation; many states similar) → state AG/consumer affairs (FL DBPR licenses CAMs) → small claims for specific money damages.
7. Keep a dated file of every letter and response — see `references/ho-escalation-ladder.md` for the evidence template.

## Common Pitfalls
1. **Missing the response deadline** while being angry — the fine becomes "valid" by default; cure-or-respond within the window even if the response is just the demand letter.
2. **Arguing fairness instead of process** — boards ignore opinions; they must answer "which covenant, adopted when, hearing held when?"
3. **Paying the fine "under protest" then fighting** — payment is often treated as acquiescence; if you pay (sometimes required to avoid liens), write "paid under protest, pending hearing" on the check and letter.
4. **Ignoring the annual meeting** — assessments and board seats are decided by the 20% of owners who show up; proxy campaigns are the cheapest structural fix.
5. **Threatening litigation early** — many states mandate ADR first (CA CIDDR), and you'll pay your own fees absent bad faith; save the lawyer letter for after the paper trail exists.

## Verification Checklist
- [ ] Response sent certified + email before deadline, copy filed
- [ ] Covenant number, adoption date, and fine schedule demanded in writing
- [ ] Hearing requested in writing (and attended if granted)
- [ ] Fine checked against state structure and adopted schedule
- [ ] Records request cited statute and inspection period
- [ ] Escalation ladder followed in order (paper trail complete)

## One-Shot Recipes
**"Photo of my trash cans, $50 fine, 10 days"** → `violation` letter demanding covenant text + hearing; 60% of these vanish at step 1 because the schedule was never adopted.
**"Special assessment $4,800 announced by email"** → `records` (reserve study, budget, meeting minutes where vote occurred), check quorum/approval threshold in bylaws — special assessments usually need a supermajority vote of the membership.
**"Assessment up 9% again"** → `assessments` 10-year projection, then open-forum statement asking for the reserve-study funding plan; run for one board seat with neighbors who sign the proxy sheet.
