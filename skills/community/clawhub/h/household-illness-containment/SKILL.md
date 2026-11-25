---
name: household-illness-containment
description: When norovirus/flu/COVID/strep/RSV/pinkeye hits one member, stop it becoming the whole household — dated, illness-specific containment protocol with exposure-watch windows for everyone else, pathogen-matched disinfection (norovirus survives quats and hand sanitizer: bleach dilutions named in cups-per-gallon, contact times included), shared-bathroom rotation rules, laundry/dish handling, return-to-school/work and food-handler clocks, high-risk member routing (infant/pregnant/65+/immunocompromised), illness-specific red flags, and the one-store-run containment kit.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [illness, norovirus, flu, contagious, family-health, isolation, infection-control]
---

# Household Illness Containment

One kid comes home with norovirus on Friday; by Wednesday the parents,
the toddler, and the grandparent are all down. Households have smoke
detectors but no containment protocol — they share bathrooms, towels,
and doom. This skill is the protocol, dated for your actual day of
illness.

## When to trigger
- "The stomach bug is going around school and my kid just started
  vomiting"
- "someone in the house has flu/COVID/strep/pinkeye — how do we not
  all get it?"
- "when can they go back to school/work?"
- "can I still cook for people while sick?"
- second-case triage: "my other kid has a sore throat — is it starting?"

## How it works

1. **Collect inputs**: illness type, first-symptom date, optionally
   symptom-free-since, today, household size, `--shared-bathroom`,
   `--food-handler`, and high-risk members (`--infant`, `--pregnant`,
   `--elderly`, `--immunocompromised`).
2. **Run** `scripts/containment_planner.py --illness norovirus
   --first-symptom 2026-11-22 --shared-bathroom`
3. **Phase engine** locates today on the illness's typical course and
   prints the exposure-watch window for the rest of the household
   (incubation band from first symptom), or the **48-hour gate** once
   symptoms stop.
4. **Pathogen-matched disinfection**: norovirus-class pathogens
   (non-enveloped) get exact bleach math — ¾ cup/gallon ≈ 5000 ppm
   for vomit/stool events, ⅓ cup/gallon ≈ 1000 ppm routine, ≥1–5 min
   contact, mixed fresh — plus the warning that quat wipes and alcohol
   sanitizer don't work. Enveloped viruses get the simpler
   any-disinfectant route.
5. **House rules**: sick room setup, shared-bathroom rotation protocol
   (sick-last + bleach pass, per-person towels, capped toothbrushes),
   kitchen and laundry handling per pathogen, dish protocol.
6. **Return clock**: illness-specific (fever-free 24 h; 48 h after
   norovirus resolution with the 48–72 h food-handler override;
   24 h of antibiotics for strep; day-5-plus-mask COVID) — dated
   against the actual course.
7. **High-risk routing + red flags + kit list** close the run.

## Pitfalls encoded
- **Alcohol hand sanitizer does not kill norovirus** — the single most
  believed wrong thing in home illness care; soap + running water
  20 s is the tool, and the output says so in caps.
- **Bleach that's months old has lost potency** — the kit list starts
  with a fresh bottle.
- **The bathroom is the battleground**: one shared towel transfers
  pinkeye through a whole family; rotation + paper towels are printed
  as explicit rules, not advice.
- **Contagiousness starts BEFORE symptoms** (flu) and continues AFTER
  (norovirus sheds ~2 weeks): the exposure-watch window and shedding
  notes encode both tails.
- **Food handlers are outbreak starters**: the 48–72 h post-norovirus
  return rule is called out as a responsibility, not a preference.
- Return clocks are **rules, not calendar promises** — fever-free
  gates apply no matter what the date says.
- Red flags per illness end the home protocol: dehydration signs,
  breathing distress, infant fever under 3 months, relapse patterns.

## Examples

```bash
# Classic: stomach bug, day 2, one shared bathroom, sick person cooks
python3 scripts/containment_planner.py --illness norovirus \
    --first-symptom 2026-11-22 --today 2026-11-24 \
    --shared-bathroom --food-handler

# Flu with a baby and a grandparent in the house
python3 scripts/containment_planner.py --illness flu \
    --first-symptom 2026-11-20 --infant --elderly

# Recovery check: symptoms stopped, when do we lift?
python3 scripts/containment_planner.py --illness norovirus \
    --first-symptom 2026-11-19 --symptom-free-since 2026-11-23 \
    --today 2026-11-25
# → SYMPTOM-FREE since 2026-11-23 — 48 h gate lifts 2026-11-25
```

## Output contract
- header: course, contagious window, household exposure-watch dates
- phase verdict (ACUTE / EXPECTED RECOVERY / 48 h-gate date)
- disinfection section matched to pathogen class (bleach math when
  needed; sanitizer verdict)
- house rules: room / bathroom / kitchen / laundry / dishes
- return clock with food-handler override, dated
- high-risk member routing, red flags, containment kit
