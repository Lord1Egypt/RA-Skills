# Interactions — Drugs, Nutrients, and What Cancels What

Two kinds of collision: a drug that changes nutrient status over months, and a nutrient that changes a drug's effect in the next hour. The first is a monitoring problem, the second is a timing problem, and confusing them produces the wrong fix.

**Before any dose or timing advice**, read the medication list in `~/Clawic/data/health/profile.md` and the current stack in `## Supplements` of `~/Clawic/data/nutrition/memory.md`. This file is unusable without both: an interaction check against an unknown medication list is theatre.

**Contents:** [The Two Failure Modes](#the-two-failure-modes) · [Drugs That Deplete Nutrients](#drugs-that-deplete-nutrients) · [Nutrients That Change a Drug](#nutrients-that-change-a-drug) · [Nutrient Versus Nutrient](#nutrient-versus-nutrient) · [Food Versus Drug](#food-versus-drug) · [The Timing Schedule](#the-timing-schedule) · [What Not to Touch](#what-not-to-touch)

## The Two Failure Modes

- **Depletion**: metformin lowering B12 over years. Slow, invisible, and fixed by scheduled monitoring — never by stopping the drug, which is not this skill's call.
- **Interference**: calcium taken with levothyroxine. Immediate, dose-relevant, and fixed by moving one of them in the day. Interference is almost always solvable by a clock, which is why the answer is a schedule and not a removal.

Anything involving warfarin, levothyroxine, methotrexate, chemotherapy, transplant immunosuppressants, antiretrovirals, or antiepileptics is a narrow-therapeutic-index drug: the check produces a *statement for the clinician*, never an adjustment (`safety.md`).

## Drugs That Deplete Nutrients

Monitoring targets, not reasons to stop a medication.

| Drug class | Depletes | Mechanism and timescale | Monitor |
|---|---|---|---|
| Metformin | B12 | Reduced ileal absorption; risk accumulates over years of use | B12 annually, MMA if borderline |
| Proton pump inhibitors | B12, magnesium, iron, calcium (carbonate) | Acid is needed to free food-bound B12, to reduce iron, and to dissolve carbonate | B12 and magnesium on long-term use; switch calcium to citrate |
| Loop and thiazide diuretics | Potassium, magnesium, zinc, thiamin | Urinary losses | Clinician monitors electrolytes; diet supports them |
| Corticosteroids, long-term | Calcium, vitamin D, potassium | Bone loss and altered handling | Bone protection is clinician-directed |
| Some antiepileptics (phenytoin, carbamazepine, phenobarbital) | Vitamin D, folate | Accelerated hepatic metabolism | Vitamin D and folate status; folate in pregnancy is a clinician conversation |
| Methotrexate | Folate | Folate antagonist by design | Folate supplementation is prescribed deliberately and dosed by the clinician — never self-added |
| Cholestyramine and bile acid sequestrants | Fat-soluble vitamins A, D, E, K | Bile acid binding | Fat-soluble vitamin status; separate dosing widely |
| Orlistat | Fat-soluble vitamins | Fat absorption blocked | Multivitamin at a separated time, per the prescriber |
| Long-term antibiotics | Vitamin K (gut synthesis) | Microbiome suppression | Relevant mainly alongside anticoagulation |
| Isoniazid | B6 | Direct antagonism | B6 is co-prescribed as standard |

## Nutrients That Change a Drug

| Nutrient | Drug affected | Effect | Fix |
|---|---|---|---|
| Vitamin K | Warfarin | Directly opposes the drug | **Consistency, not avoidance.** A stable weekly intake of greens is manageable; the swings are what destabilize INR. Any planned change goes to the anticoagulation clinic first |
| Calcium, iron, magnesium | Levothyroxine | Bind it in the gut and cut absorption | Levothyroxine fasting, ≥4 hours from all three |
| Calcium, iron, magnesium, zinc | Tetracyclines, fluoroquinolones | Chelation | 2 hours before, 4-6 hours after the antibiotic |
| Potassium (supplements or salt substitutes) | ACE inhibitors, ARBs, potassium-sparing diuretics | Additive hyperkalemia risk | No potassium supplements or potassium-chloride salt substitutes without clinician approval |
| Vitamin E, omega-3 at high dose, vitamin K | Anticoagulants and antiplatelets | Bleeding risk modification in both directions | Clinician review before any dose above ordinary dietary levels |
| Folic acid above 1000 µg | Masks B12 deficiency; interacts with methotrexate | Blood picture corrects while nerve damage advances | B12 status before folate, always |
| Iron | Levothyroxine, some antibiotics, bisphosphonates | Binding | Separate as above |
| High-dose vitamin C | Some assays and, at gram doses, oxalate load | GI distress and kidney stone risk in susceptible people | Keep below the 2000 mg UL absent a clinician reason |
| Biotin, high dose | Laboratory immunoassays, not the drug | False highs and lows including thyroid and troponin | Stop 48-72 h before blood work and tell the lab (`labs.md`) |

## Nutrient Versus Nutrient

| Pair | What happens | Practical rule |
|---|---|---|
| Zinc ↔ copper | Sustained zinc above ~40 mg/day induces intestinal metallothionein, which traps copper — deficiency follows | Cap the stack sum at the UL; a long zinc course watches copper |
| Iron ↔ calcium | Compete at absorption | Separate by ≥2 hours; never in the same tablet expectation |
| Iron ↔ zinc | Compete when taken together in supplement doses | Separate doses; food-level amounts are not the problem |
| Calcium ↔ magnesium | Modest competition at high supplement doses | Split them across the day if both are supplemented |
| Vitamin C ↔ non-heme iron | Enhancement, the useful one | Deliberately pair them in the same meal (`absorption.md`) |
| Folate ↔ B12 | Folate masks the hematologic sign of B12 deficiency | Order of operations: B12 first, always |
| Vitamin D ↔ calcium | D raises calcium absorption | High-dose D plus high-dose calcium is where hypercalcemia comes from — sum both |
| Vitamin A ↔ vitamin D | Some antagonism at high intakes | Relevant only when both are supplemented at high doses |
| Phytate, oxalate, tannins ↔ iron, zinc, calcium | Inhibition within the meal | Meal composition and timing, covered fully in `absorption.md` |

## Food Versus Drug

- **Grapefruit** inhibits intestinal CYP3A4 and raises blood levels of several statins, some calcium channel blockers, and certain immunosuppressants. The effect lasts many hours, so "take them apart" does not work — the fruit is avoided or the drug is changed, and it is the prescriber's call.
- **Tyramine-rich foods** (aged cheese, cured meats, some fermented products) with MAO inhibitors: a hypertensive crisis risk, and the diet is prescribed with the drug.
- **Alcohol** interacts with more medications than any food, and independently depletes thiamin, folate, B6, magnesium, and zinc.
- **High-fiber meals and viscous fiber supplements** can slow the absorption of some drugs: separate a psyllium dose from medication by ~2 hours as a default.
- **Cranberry, pomegranate, and green tea extract** appear in warfarin and other interaction lists; concentrated extracts are the concern, not the ordinary glass.

## The Timing Schedule

When two or more separations apply, build one schedule rather than issuing rules one at a time. A schedule the user can follow beats a correct list they cannot.

Worked example — levothyroxine, iron repletion, calcium 1000 mg, vitamin D:

| Time | Take | Why |
|---|---|---|
| On waking, fasting | Levothyroxine | Needs an empty stomach and ≥4 h from calcium and iron |
| Breakfast +1 h | Iron, alternate days, with orange juice | ≥4 h clear of levothyroxine, vitamin C paired, no tea or coffee within the hour |
| Lunch | Calcium 500 mg + vitamin D | Split dose at the absorption ceiling, D with the meal's fat |
| Dinner | Calcium 500 mg | Second half of the split, far from the iron dose |

Write the finished schedule to `artifacts/supplement-schedule.md` when it has three or more moving parts — it is exactly the kind of thing that gets reconstructed badly from memory.

## What Not to Touch

- Never advise stopping, splitting, or changing the dose of a prescribed medication. The output is a timing schedule and a statement to bring to the prescriber.
- Never add folate, potassium, vitamin K, or iron to a picture involving methotrexate, potassium-sparing drugs, warfarin, or unexplained high ferritin.
- Never treat an interaction as resolved because a symptom improved; INR, TSH, and potassium are laboratory questions.
- When two credible sources conflict on an interaction, say so and route to the pharmacist — pharmacists own this question and are the most accessible clinician for it.

**Write in the same turn**: any depletion risk found (metformin → B12, PPI → magnesium) as a monitoring row in `## Due` and a note on the nutrient's `## Nutrient Status` row; any timing separation into the affected `## Supplements` rows; a schedule with three or more moving parts into `artifacts/supplement-schedule.md` with its `## Boxes` line; and any medication learned during the session into `~/Clawic/data/health/profile.md` (`memory-template.md`).
