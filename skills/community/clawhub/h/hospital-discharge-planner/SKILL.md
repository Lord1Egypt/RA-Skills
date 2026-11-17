---
name: hospital-discharge-planner
description: Use when a family member is being discharged from the hospital — audits the discharge order BEFORE signing (the 7 questions that catch unsafe discharges: follow-up booked? meds reconciled? new equipment trained? who calls if X?), decodes the paperwork stack (NOF vs discharge instructions vs AVS), runs the post-acute decision map (home with help vs SNF vs rehab — Medicare 3-night rule and the Day-21 therapy cliff), builds the 72-hour landing-zone plan (meds schedule, red-flag sheet for caregivers, first follow-up visit logistics), and generates the caregiver handoff card + questions-for-the-case-manager list.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [hospital, discharge, caregiving, medicare, patient-advocacy, post-acute, snf]
---

# Hospital Discharge Planner

Discharge day is the most dangerous handoff in medicine: the patient
moves from 24/7 monitored care to a home setup decided in a 15-minute
conversation, on a medication list that may have been rewritten twice
that week, with follow-up appointments that "someone will call to
schedule." Readmissions within 30 days run ~15% — and most discharge
harm is preventable with questions asked BEFORE the wheelchair reaches
the lobby.

## When to Use

- Discharge is announced today/tomorrow — before the papers are signed
- Deciding post-acute setting: home vs rehab (SNF/IRF) vs assisted
  living respite
- A Medicare patient crossing the 3-night observation-vs-admission line
  (SNF coverage depends on it)
- Setting up the home landing zone: meds, equipment, bedroom floor,
  first 72 hours of caregiving
- Second opinion on "ready for discharge" when the family disagrees
- Caregiver handoff between family members / hired help

**Don't use for:** disputing an inpatient admission actively needed
(ask for the medical team); discharges to hospice (a different, palliative
playbook — ask for the hospice coordinator); pediatric NICU protocols
(hospital-specific). If the patient is unsafe to be discharged, say the
words "I want to file an appeal under MOON/IMD" — see references.

## The Method

1. **`audit`** — the 7-question discharge-order audit asked BEFORE
   signing: (1) meds reconciled against the home list — every change
   named and why; (2) follow-up appointments BOOKED with dates, not
   "will call"; (3) new equipment/services ordered AND trained; (4)
   red-flag symptoms for THIS condition with who-to-call numbers;
   (5) activity/wound/diet orders in writing; (6) who is the
   responsible clinician between now and follow-up; (7) is the
   destination actually ready (person + meds + bed level + ride)?
   Any "no" = a gap to close before the wheelchair moves.
2. **`paperwork`** — decode the document stack: After-Visit Summary
   (AVS) vs discharge instructions vs Notice of Medicare Non-Coverage
   (NOF/CMS-10123) vs the MOON observation notice; which pieces the
   next-of-kin should keep; where the diagnosis and med list live for
   the next ER visit (pro tip: photo of every page).
3. **`postacute --nights 4 --setting home-with-help`** — the setting
   decision: home-with-help vs SNF vs IRF with the Medicare mechanics
   (3-night inpatient rule for SNF; days 1–20 fully covered, days
   21–100 daily coinsurance 2026, the "therapy cliff" where SNF stops
   progress-gains); home-health eligibility (homebound + skilled need);
   what "observation status" breaks.
4. **`landing --help-hours 8 --floors 1`** — the 72-hour landing plan:
   med-schedule build (reconciled list → times grid, first dose timing),
   bedroom-floor setup (bathroom distance, night path lighting, chair
   height), caregiving coverage vs your hours, the red-flag sheet on
   the fridge, first follow-up transport.
5. **`handoff`** — generates the caregiver handoff card (conditions,
   meds with times, allergies, red flags + numbers, code status,
   PCP/specialist) and the case-manager question list.

Run `python3 scripts/discharge_planner.py <cmd> --help`.

## Judgment Rules

- **Discharge is a negotiation, not a verdict.** If the patient is
  unsafe (can't transfer, no caregiver, uncontrolled pain), say it out
  loud and ask for: case manager, discharge planner, or a delayed
  discharge. Filing the NOF appeal fast-forwards the conversation.
- **"Someone will call to schedule" = not booked.** Unbooked follow-up
  is the #1 discharge gap; get the appointment date in writing, or
  call from the hospital room before leaving — with the insurance
  card, hospital scheduling desk does it faster than you will later.
- **The med list is the danger zone.** Hospitals restart chronic med
  lists from scratch; home meds get dropped or duplicated (especially
  blood thinners, diabetes meds, diuretics). Reconcile line by line
  against the HOME pharmacy list; ask "start/stop/changed?" per drug.
- **Observation status quietly costs $ thousands.** Medicare
  observation ≠ inpatient: no SNF coverage, different Part B cost
  sharing. Ask DAILY "what is the patient's status today?" and if
  observation, ask the case manager to reconsider (or request
  Beneficiary and Family Centered Care review).
- **Home-health orders must exist before you leave.** "We'll order
  home health" verbal = nothing; get the agency name and the order in
  the AVS.
- **The 72-hour landing zone fails on logistics, not medicine:**
  nobody picked up the new prescription, the bedroom is upstairs, the
  caregiver shifts don't cover night wander-risk. `landing` exists to
  make those explicit.
- **Photo every page of the paperwork.** The next ER/urgent visit runs
  10× smoother with the AVS on your phone.

## Common Pitfalls

1. Signing discharge papers as-is without the 7-question audit — gaps
   surface at home at 11 pm, not in the suite.
2. Assuming follow-up is scheduled. It isn't until it has a date and a
   name.
3. Missing med reconciliation: home beta-blocker "disappeared" from
   the new list; duplicate PPIs; insulin scale changed without the
   family being told.
4. Observation status discovered AFTER the SNF bill — nobody asked
   status during the stay.
5. Fighting for SNF days 21–100 without progress documentation —
   therapy notes are the currency; ask for them weekly.
6. The landing zone built around an optimistic mobility estimate —
   plan for the discharge-day reality, upgrade later.
7. No red-flag sheet — every caregiver invents their own "should we
   call?" threshold; the sheet standardizes it.
8. Ride home arranged for the wrong time ("discharge at 10" often
   means 16:00) — ask for the realistic window the morning of.

## Verification Checklist

- [ ] 7-question audit asked; every gap has an owner and a time
- [ ] Med list reconciled line-by-line vs home pharmacy list; changes
      understood (start/stop/dose) in writing
- [ ] Follow-up appointments: dates + names in hand (not "will call")
- [ ] Home health / equipment / DME: ordered, named, trained
- [ ] Patient status confirmed (inpatient vs observation) in writing
- [ ] Post-acute setting decided with the Medicare math understood
- [ ] Red-flag sheet printed and on the fridge; numbers verified
- [ ] 72-hour landing plan: meds picked up, bedroom floor set, night
      coverage assigned, first-visit transport booked
- [ ] Every paperwork page photographed
- [ ] Handoff card given to every caregiver (family + hired)

## One-Shot Recipe

Mom, 78, hip replacement, day 3, discharge tomorrow, Medicare
Advantage, family covering evenings:

```bash
python3 scripts/discharge_planner.py audit
python3 scripts/discharge_planner.py paperwork
python3 scripts/discharge_planner.py postacute --nights 3 --setting home-with-help
python3 scripts/discharge_planner.py landing --help-hours 6 --floors 1
python3 scripts/discharge_planner.py handoff --patient "Mom 78, hip replacement" \
    --contact "Ana (daughter) 555-0100"
```

Ask the audit questions at today's rounding; get the PT follow-up and
home-health order INTO the AVS before the wheelchair moves.
