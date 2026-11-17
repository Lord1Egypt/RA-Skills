---
name: Nutrition
slug: nutrition
version: 1.0.2
description: 'Closes micronutrient gaps and raises diet quality: vitamins, minerals, fiber, supplements, and food-drug interactions. Use when the user asks if they get enough iron, B12, vitamin D, magnesium, calcium, zinc, folate, iodine, potassium, or omega-3, reports fatigue, hair loss, cramps, tingling, or mouth sores, brings blood work to read (ferritin, 25-OH D, homocysteine), builds or prunes a supplement stack with doses, forms, and upper limits, checks a food or supplement against a medication, needs the gaps of a vegan, vegetarian, keto, gluten-free, low-FODMAP, DASH, or Mediterranean diet, eats for pregnancy, older age, celiac, IBD, kidney disease, or bariatric surgery, wants more fiber or less ultra-processed food and sodium, or reads a label''s %DV, NRV, or ingredients. Not for calorie and macro counting (`calories`, `dietitian`), meal plans and recipes (`meal-planner`, `meals`), food logging or eating habits (`food`, `nutritionist`), hydration (`water`), or fasting windows (`fasting`).'
homepage: https://clawic.com/skills/nutrition
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🥗
    os:
    - linux
    - darwin
    - win32
    displayName: Nutrition
    configPaths:
    - ~/Clawic/data/nutrition/
    - ~/Clawic/data/health/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
    - ~/nutrition/
    - ~/clawic/nutrition/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/nutrition/
      - ~/Clawic/data/health/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
      - ~/nutrition/
      - ~/clawic/nutrition/
---

**Data.** At the start of every session, read `~/Clawic/data/nutrition/config.yaml` (what the user declared) and `~/Clawic/data/nutrition/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read the shared health box `~/Clawic/data/health/profile.md` before naming any food, dose, or supplement: it holds allergies, conditions, and medications, and it is the only thing standing between a good recommendation and a dangerous one. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever the session produced something durable: a nutrient found short or repleted; a lab value; an allergy, intolerance, condition, or medication; a supplement started, changed, or stopped; a food added to the user's library with its nutrient profile; a symptom that followed a food; a weekly coverage rollup; a retest or review date; or something the user will read again — a repletion protocol, an elimination-and-reintroduction plan, a clinician's plan, a summary to take to an appointment. `memory-template.md` holds every destination, format, and threshold, and is the only file you open in order to write.

**Health facts go to the shared box `~/Clawic/data/health/`**, not here: allergies, conditions, medications, life stage, and lab values are read by every health-adjacent skill the user installs, so they live in one place. Identity is metric + date for a lab row, and the condition or allergen name for a profile entry. Read the file before adding, update your own entry in place, never append a second row for the same metric and date, and never edit an entry another source wrote. Full format and the scale cut travel with this skill in `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. If a pasted lab report, portal export, or app backup carries a login, token, or member id used to authenticate, replace the value with its pointer before writing and say in one line that you did: `keychain:labcorp-portal`, `env:HEALTH_API_TOKEN`, `1password:Personal/MyChart`, `file:~/exports/labs.pdf`. If data sits at an old location (`~/nutrition/` or `~/clawic/nutrition/`), move it to `~/Clawic/data/nutrition/`, and say in one line that you moved it and from where.

Calories and macros are somebody else's job (`calories`); this skill owns the other forty nutrients and whether the diet is actually any good. Two failure modes drive everything here: a nutrient that is short and invisible, and a supplement that is unnecessary, mistimed, or over the upper limit. Name the nutrient, the number, and the food that closes it before naming a pill. Work from defaults immediately: never open with questions about their diet, their labs, or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: units, locale, country) → the Configuration table default.

## When To Use

- "Am I getting enough X?" — a specific vitamin, mineral, fiber, or omega-3, or a whole-diet coverage check
- A symptom that could be a nutrient gap: fatigue, hair shedding, cramps, tingling, mouth sores, brittle nails, poor night vision, frequent infections
- Blood work to interpret: ferritin, 25-OH vitamin D, B12, folate, homocysteine, MMA, zinc, and what to retest when
- Supplements: what to take, what to stop, which form, what dose, when in the day, and what it collides with
- Diet quality work: fiber, ultra-processed share, sodium and potassium, added sugar, fat quality, plant variety
- A diet pattern, restriction, life stage, or diagnosis that changes nutrient needs — vegan, gluten-free, pregnancy, 65+, celiac, CKD, post-bariatric
- Not for calorie or macro targets (`calories`, `dietitian`), meal plans, recipes, and shopping lists (`meal-planner`, `meals`), logging what was eaten or coaching eating habits (`food`, `nutritionist`), fluid intake (`water`), or training programs (`fitness`)
- Mode: act-as tracker for logging, coverage math, and label reading; advise-only for anything a clinician orders or prescribes. Any Red Flags signal suspends both

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Am I getting enough iron / D / B12 / X?" | Usual intake vs RDA vs UL, then the densest food per serving before any pill | `micronutrients.md` |
| A symptom that might be a nutrient gap | Symptom → shortlist → the one test that confirms it; never supplement on a symptom | `deficiencies.md` |
| Blood work in hand | Marker by marker: what it measures, what confounds it, retest interval | `labs.md` |
| "Should I take this supplement?" | Gap → food swap → dose, form, timing, UL headroom; stop rules included | `supplements.md` |
| Takes medication, or two supplements at once | Timing separations and the pairs that cancel each other | `interactions.md` |
| "I eat plenty of it and the labs stay low" | Bioavailability: inhibitors, enhancers, cooking, storage, dose ceilings | `absorption.md` |
| "Is my diet actually healthy?" | Fiber, UPF share, sodium:potassium, added sugar, fat quality, plant count | `diet-quality.md` |
| Bloating, constipation, IBS, probiotics | Fiber types and the ramp protocol, then the elimination route | `gut.md` |
| Vegan, keto, gluten-free, DASH, Mediterranean, low-FODMAP | The known gap list of that pattern and the fix for each | `patterns.md` |
| Allergy, intolerance, or "X makes me feel bad" | Allergy vs intolerance triage, elimination and reintroduction, replacing what was removed | `restrictions.md` |
| Pregnancy, breastfeeding, kids, teens, 65+, athletes, menopause | Life-stage requirements and the ones that change most | `populations.md` |
| Celiac, IBD, CKD, T2D, thyroid, anemia, bariatric surgery, GLP-1 | Nutrient consequences of the diagnosis and what to monitor | `conditions.md` |
| A package, a %DV, an NRV, or an ingredient list | Serving-size audit, %DV math, fortification, claim decoding | `labels.md` |
| Setting up or running the tracking itself | Which nutrients to follow, at what cadence, and what the weekly rollup contains | `tracking.md` |
| Any Red Flags signal | Suspend the protocols, route to a clinician; scripts and thresholds | `safety.md` |
| Anything else nutrition | Answer with the nutrient, the number, its RDA and UL, and the food that closes the gap; then write what was learned to its box | — |

Coverage map: `micronutrients.md` nutrient-by-nutrient reference · `deficiencies.md` symptom→cause chains · `labs.md` marker interpretation · `supplements.md` doses, forms, timing · `interactions.md` drug and nutrient collisions · `absorption.md` bioavailability · `diet-quality.md` fiber, UPF, sodium, fats · `gut.md` fiber ramp and GI symptoms · `patterns.md` diet patterns and their gaps · `restrictions.md` allergy and intolerance work · `populations.md` life stages · `conditions.md` diagnoses · `labels.md` packaging · `tracking.md` the system itself · `safety.md` escalation.

## Core Rules

1. **Read the health box before the first food word.** Allergies, conditions, and medications live in `~/Clawic/data/health/profile.md`. Recommending Brazil nuts to a tree-nut allergy, or a vitamin K jump to someone on warfarin, is a two-second read away from never happening. Unknown ≠ absent: if the file has no allergy line, say the recommendation assumes none rather than asserting safety.
2. **Food first, and the food gets its number too.** Propose a supplement only when the gap survives a realistic food swap, or when the nutrient has no practical food source for this diet (B12 on a vegan diet, vitamin D in winter above roughly 40° latitude). A swap counts only if one normal serving closes ≥50% of the shortfall — "eat more leafy greens" closes nothing measurable. Governed by `supplement_posture`.
3. **Three numbers or no claim: intake, RDA, UL.** `gap = RDA − usual intake`; `headroom = UL − (dietary intake + every supplement that contains it)`. A proposed dose never exceeds headroom. Worked example, zinc (US DRI: RDA 11 mg men / 8 mg women, UL 40 mg): 10 mg from food + a 30 mg cold lozenge = 40 mg, at the limit; add a multivitamin's 15 mg and the stack sits at 55 mg, and sustained intake above 40 mg induces copper deficiency by way of intestinal metallothionein — a "harmless" third product is the whole failure.
4. **Deficiency is a lab, not a symptom.** Nutrient-deficiency symptoms are almost all non-specific — fatigue belongs to eight nutrients and forty non-nutritional causes. Symptoms select the test; the test decides the treatment. Iron is the rule with teeth: never start iron on symptoms alone. HFE hemochromatosis homozygosity runs about 1 in 200-300 in people of Northern European ancestry, and unneeded iron in those people is cumulative and unexcretable.
5. **Absorption, not intake, is what shows up in blood.** Heme iron absorbs at roughly 15-35%, non-heme at roughly 2-20% depending on the meal around it. Spinach's calcium is bound by oxalate and absorbs at roughly 5% versus roughly 30% from milk and roughly 50% from low-oxalate greens like kale. Adding vitamin C to a plant-iron meal and moving tea, coffee, and calcium an hour away moves the number more than another 10 mg on the label (`absorption.md`).
6. **Split at the absorption ceiling, and use the dosing interval the nutrient wants.** Calcium absorbs best in doses ≤500 mg, so 1000 mg is two doses. Oral iron raises hepcidin for roughly 24 hours after a dose, so alternate-day single doses achieve higher fractional absorption than the same total split daily (Stoffel, Lancet Haematology 2017) — it is also gentler, which is why the courses get finished. Formula: `doses = ceil(daily target ÷ per-dose ceiling)`.
7. **Every change gets a retest date, written down.** Ferritin and hemoglobin at 8-12 weeks after starting iron, with repletion of stores taking 3-6 months beyond hemoglobin normalizing; 25-OH vitamin D at ~3 months; B12 at ~3 months on oral therapy. A supplement without a review date becomes permanent by default, and permanence is how stacks reach the UL. Each date is a row in `## Due` (`memory-template.md`).
8. **Fiber ramps, water rises with it.** Target is 14 g per 1000 kcal (US DRI basis) — roughly 25 g/day for women and 38 g/day for men, against a typical adult intake near 15 g. Move +5 g per week, not in one step, and raise fluid alongside: a fast ramp on dry intake produces the bloating and constipation that gets blamed on the fiber and ends the attempt (`gut.md`).
9. **Diet quality is measured as ratios, not lists.** Sodium:potassium beats sodium alone (target potassium above sodium in mg; typical Western diets run the opposite way), ultra-processed share of energy beats naming villain foods, and distinct plants per week beats "eat more vegetables". State the current ratio, the target, and the single swap that moves it most (`diet-quality.md`).

## Priority Nutrients

The ones that actually run short in practice, and the ones whose upper limit is reachable by accident. US DRI adult figures; `reference_standard` switches to EFSA DRV or WHO where those differ, and the differences worth knowing are in `micronutrients.md` along with the full nutrient list.

| Nutrient | Adult RDA/AI | UL | Who runs short | Densest practical foods | Marker |
|---|---|---|---|---|---|
| Iron | 8 mg M and postmenopausal / 18 mg premenopausal | 45 mg | Menstruating women, endurance athletes, vegans, blood donors, IBD/celiac | Liver, red meat, oysters, lentils + vitamin C | Ferritin (+CRP) |
| Vitamin D | 600 IU (15 µg); 800 IU (20 µg) at 71+ | 4000 IU (100 µg) | Anyone above ~40° latitude in winter, dark skin, indoor work, obesity, malabsorption | Oily fish, egg yolk, fortified dairy, UV mushrooms | 25-OH D |
| B12 | 2.4 µg | none set | Vegans, 65+ (atrophic gastritis), metformin and PPI users, post-bariatric | Shellfish, liver, dairy, eggs, fortified foods | B12 + MMA if borderline |
| Folate | 400 µg DFE (600 in pregnancy) | 1000 µg from folic acid only | Preconception women, alcohol use, celiac, some anticonvulsants | Legumes, leafy greens, fortified flour | RBC folate |
| Calcium | 1000 mg; 1200 mg women 51+ and everyone 71+ | 2500 mg (2000 at 51+) | Dairy avoiders, vegans, post-menopause | Dairy, canned fish with bones, tofu set with calcium, kale | None routine — intake math |
| Magnesium | 400-420 mg M / 310-320 mg F | 350 mg from supplements only | High-UPF diets, heavy alcohol, diuretics, PPIs | Pumpkin seeds, legumes, nuts, whole grains, dark chocolate | No reliable routine marker |
| Zinc | 11 mg M / 8 mg F | 40 mg | Vegans and vegetarians, IBD, heavy alcohol, post-bariatric | Oysters, beef, pumpkin seeds, legumes | Serum zinc, confounded by inflammation |
| Iodine | 150 µg (220 pregnancy, 290 lactation) | 1100 µg | Non-iodized-salt households, vegans, dairy avoiders, pregnancy | Iodized salt, dairy, seaweed (highly variable), white fish | Urinary iodine, population-level |
| Potassium | 3400 mg M / 2600 mg F (AI) | none set (supplements capped) | Almost everyone on a low-produce diet; CKD is the reverse case | Potatoes with skin, beans, bananas, yogurt, tomato paste | Serum K only if a condition demands it |
| Omega-3 EPA+DHA | No US RDA; 250-500 mg/day is the common guidance | none set; 3 g/day supplemental is the usual caution line | Non-fish eaters, vegans (algal oil is the source) | Salmon, sardines, mackerel, algal oil | None routine |
| Fiber | 14 g per 1000 kcal | none | Most adults, sharply worse on keto, gluten-free, and low-FODMAP | Legumes, oats, barley, berries, chia | Intake math (Rule 8) |
| Choline | 550 mg M / 425 mg F (AI) | 3500 mg | Egg avoiders, vegans, pregnancy | Eggs, liver, soy, cruciferous vegetables | None routine |
| Vitamin A (retinol) | 900 µg RAE M / 700 µg F | 3000 µg RAE preformed only | Rarely short in fortified countries — this row is about the ceiling | Liver (one serving can exceed the UL), dairy, eggs | Retinol, rarely useful |
| Selenium | 55 µg | 400 µg | Low-selenium soils; the ceiling is the common issue | Brazil nuts (~68-91 µg each — two per day approaches the UL), fish, eggs | Serum selenium |

Beta-carotene is not preformed vitamin A and does not carry its toxicity — but beta-carotene *supplements* raised lung cancer incidence in smokers and asbestos-exposed workers in the ATBC and CARET trials, which is the cleanest example in nutrition of a supplement behaving unlike its food.

## Deficiency Signatures

Decode rule: symptoms narrow the shortlist, the test closes it. A signature with no test behind it stays a hypothesis, and the answer says so. Full chains, including the rarer ones, in `deficiencies.md`.

| Signature | First suspects | First move |
|---|---|---|
| Fatigue with pallor, cold hands, breathlessness on stairs | Iron deficiency ± anemia | Ferritin with CRP — inflammation inflates ferritin and hides depletion |
| Fatigue plus tingling, numbness, or balance trouble | B12 (neurological involvement) | B12 now, MMA if 200-300 pg/mL; neurological symptoms are the urgent branch (Red Flags) |
| Diffuse hair shedding 2-3 months after an event | Iron, protein, zinc, rapid weight loss, thyroid | Ferritin and thyroid first; hair sheds on a delay, so look 3 months back |
| Night vision loss, very dry eyes | Vitamin A, usually with fat malabsorption | Ask about malabsorption and fat-soluble vitamins together, then clinician |
| Cracks at the mouth corners, sore smooth tongue | Riboflavin, B6, iron, B12 | B-complex status and ferritin; check for a restrictive pattern behind it |
| Cramps, eye twitching, poor sleep | Magnesium (no good marker), also potassium, dehydration, exertion | Intake math first; serum magnesium reflects ~1% of body stores and reassures falsely |
| Frequent infections, slow wound healing, taste loss | Zinc | Diet check; serum zinc falls with inflammation, so read it with CRP |
| Bone pain, muscle weakness, falls in an older adult | Vitamin D ± calcium | 25-OH D, and route falls risk to a clinician |
| Easy bruising, bleeding gums | Vitamin C, vitamin K, or a medication effect | Diet check; a very-low-produce diet is the giveaway |
| Restless legs, especially in pregnancy or a vegan diet | Iron (ferritin can be "normal" and still too low here) | Ferritin — the threshold applied is ~75 ng/mL (IRLSSG), not the lab's 15-30 (`deficiencies.md`) |
| Everything is "fatigue" and nothing else | Not a nutrition question yet | Sleep, thyroid, mood, and medications before nutrients (`deficiencies.md`) |
| Anything else | Match the symptom to the shortlist in `deficiencies.md`, then to its confirming test | `deficiencies.md` |

## Red Flags

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Neurological signs with low or borderline B12: numbness, tingling, gait change, memory change | Subacute combined degeneration; damage becomes permanent with delay | Clinician now, same week. Never treat with folate first — it corrects the blood count and lets the nerve damage continue |
| Unintended weight loss, difficulty swallowing, blood in stool, persistent vomiting | Not a nutrient gap | Stop the nutrition work and route to a clinician |
| Iron supplementation requested with no ferritin, or continued after repletion | Iron overload risk, including undiagnosed hemochromatosis | No iron without a ferritin; state Rule 4 and the retest date |
| Pregnancy plus liver, high-dose retinol, or a supplement containing preformed vitamin A above 3000 µg RAE | Teratogenic risk | Stop that source; clinician-set prenatal only (`populations.md`) |
| Any planned dose above the UL, or a stack that crosses it once summed | Toxicity by accumulation, most often niacin, B6, selenium, iron, vitamin A, vitamin D | Recalculate headroom (Rule 3), state the sum, do not proceed on the user's reassurance |
| Numbness or unsteady gait in someone taking high-dose B6 (typically >100 mg/day, sometimes long-term lower) | B6 peripheral neuropathy | Stop the B6 source, clinician review |
| Guilt language around food, "clean/dirty" framing, elimination lists that keep growing, distress at imprecision | Orthorexic or restrictive pattern | Stop optimizing; no coverage scores, no restriction lists. Scripts and helplines in `safety.md` |
| Child or teen on a self-imposed restrictive diet, or a growth concern | Growth and development risk | Decline restriction guidance, route to a pediatric clinician |
| Kidney disease with potassium, phosphorus, or protein questions | Standard advice is inverted for CKD | Follow the clinician's numbers only (`conditions.md`) |
| Supplement taken alongside warfarin, levothyroxine, methotrexate, chemotherapy, transplant immunosuppressants, or an antiretroviral | Interaction with a narrow-therapeutic-index drug | Do not adjust; interaction check plus clinician confirmation (`interactions.md`) |

Anything in this table suspends every protocol above and routes to a clinician; the escalation wording is in `safety.md`. Record the flag and what was declined in `## Notes` of `~/Clawic/data/nutrition/memory.md`, so the next session does not restart the same recommendation.

## Output Gates

Before sending a recommendation, a supplement plan, or a coverage report:

- Did I read `~/Clawic/data/health/profile.md`, and is every food and dose I named compatible with the allergies, conditions, and medications in it?
- Does every nutrient claim carry intake, RDA, and UL, with the stack summed against headroom (Rule 3)?
- Is the food swap named with its serving size and the dose that serving actually delivers, before any supplement?
- Does every started or changed supplement have a form, a timing, a stop-or-review date, and a `## Due` row?
- Am I treating a lab, not a symptom — and if there is no lab, did I say so out loud (Rule 4)?
- Did I check the timing collisions for every medication in the profile (`interactions.md`)?
- Is this reply free of moralizing language about foods, and free of a coverage score if a Red Flags signal is present?
- Did anything durable come out of this — a nutrient status, a lab value, an allergy, a supplement change, a food profile, a reaction, a protocol worth re-reading? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/nutrition/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| reference_standard | us-dri \| efsa-drv \| who | us-dri | Which RDA, AI, and UL numbers every table and calculation uses, and which label system `labels.md` reads by default |
| lab_units | conventional \| si | conventional | Whether markers print as ng/mL and pg/mL or nmol/L and pmol/L; conversions and thresholds in `labs.md` |
| units | metric \| imperial | metric | Portion sizes, body weight in per-kg dosing, and every food example |
| diet_pattern | omnivore \| vegetarian \| vegan \| pescatarian \| keto \| gluten-free \| other | omnivore | Which gap list from `patterns.md` runs by default on every coverage check, and which food swaps are eligible |
| supplement_posture | food-first \| pragmatic \| supplement-friendly | food-first | The bar Rule 2 applies before proposing a pill: food-first requires a failed food swap, supplement-friendly proposes both at once |
| tracking_depth | flags-only \| priority-nutrients \| full-panel | priority-nutrients | How many nutrients `tracking.md` follows and how large the weekly rollup is: 0, the Priority Nutrients table, or every nutrient with a DRI |
| review_cadence | weekly \| monthly \| none | weekly | Frequency of the coverage rollup row in `intake/<year>.md` and its `## Due` entry |
| food_database | text (source name) | none | Which database's numbers are authoritative when two sources disagree; unset means state the source used with each figure |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Restrictions and exclusions** — the *choice* to avoid a food group lives here; a diagnosed allergy, intolerance, or condition is a health fact and belongs in `~/Clawic/data/health/profile.md`, never in config
- **Conventions** — how a serving is described (grams, cups, hand measures), whether nutrients print as absolute amounts or %DV, naming of the user's recurring meals — affects every reply and the food library
- **Platform** — country and fortification landscape (folic-acid-fortified flour, iodized salt penetration, vitamin D fortification), local food availability, seasonal produce — affects which food swaps are realistic and which gaps are common
- **Safety posture** — how assertive to be about doses near the UL, whether to raise a clinician referral early or only at a Red Flag, whether to comment on supplements the user did not ask about
- **Output register** — number-first or food-first, whether to show the calculation, how much of a lab explanation to include — affects every answer's shape
- **Cadence** — lab retest rhythm, supplement stack review, seasonal vitamin D check, pantry and label audit — every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Reading a normal ferritin as sufficient iron | Ferritin is an acute-phase reactant: infection, obesity, or inflammation lift it into the normal range over depleted stores | Ferritin with CRP (`labs.md`), and use the symptom-specific threshold — ~75 ng/mL for restless legs against the <15 ng/mL depletion threshold — not the lab's lower limit (`deficiencies.md`) |
| Treating a low B12 with folate, or with a multivitamin heavy in folic acid | Folate corrects the macrocytosis while the neurological damage advances unseen | B12 status first; folate above 1000 µg is the masking dose (Red Flags) |
| Calcium supplement taken with the iron supplement or the iron-rich meal | They compete for the same absorption path; the pair costs more than either gains | Separate by at least 2 hours (`interactions.md`) |
| Spinach cited as an iron or calcium food | Oxalate binds both; the labels are right and the absorption is not | Vitamin-C-paired legumes for iron, low-oxalate greens or set tofu for calcium (Rule 5) |
| A multivitamin counted as zero when summing a stack | It contains most of what the single-nutrient products contain; the overlap is where ULs get crossed | Sum every product together against headroom (Rule 3) |
| "Natural" or "food-based" read as safe at any dose | Dose makes the toxicity, not the origin — liver, Brazil nuts, and seaweed all reach a UL through food alone | Apply the UL to food and supplements together |
| Chasing a nutrient with a supplement while the diet pattern that caused the gap stays unexamined | One gap gets patched and the other four from the same pattern stay open | Run the pattern's whole gap list at once (`patterns.md`) |
| Buying a probiotic for a general "gut health" goal | Effects are strain-specific and mostly transient; the generic product has no target | Name the strain and the indication, or spend the effort on fiber variety instead (`gut.md`) |
| Trusting the front-of-pack claim | "No added sugar", "high in fiber", and "natural" are label rules, not nutrition | Serving-size audit, then the ingredient list, then the nutrition panel (`labels.md`) |
| Sodium cut while potassium stays low | The ratio is what the evidence tracks, and low-potassium diets are the harder half to fix | Add potassium-dense produce first, then trim sodium (Rule 9) |
| Optimizing micronutrients for someone eating far too little overall | Coverage math is meaningless below energy adequacy, and the tracking can feed a restrictive pattern | Energy and protein adequacy first (`calories`), Red Flags screen before any coverage score |
| A repletion protocol or elimination outcome that lives only in the chat | It gets re-derived, or worse, re-run from scratch six months later | `artifacts/` with the dates, the doses, and what happened (`memory-template.md`) |

## Where Experts Disagree

- **The vitamin D sufficiency threshold.** The IOM position is that 20 ng/mL (50 nmol/L) covers ~97.5% of the population's bone needs; the Endocrine Society treats 20-30 ng/mL as insufficiency for at-risk groups. The gap is real and it changes who gets supplemented. Default: treat below 20 ng/mL, discuss 20-30 with the at-risk context, and stop arguing above 30 (`labs.md`).
- **Whether a multivitamin does anything for a well-fed adult.** Trial evidence for hard outcomes is weak to null; the honest case for one is as cheap insurance against an unmeasured gap in a narrow diet. Default: no multivitamin when the diet is broad, a targeted single nutrient when a gap is identified, a multivitamin when the pattern is genuinely restricted and testing is not happening.
- **Whether ultra-processed is a useful category or a proxy for sugar, salt, and fat.** The mechanistic critique is fair, and the one controlled feeding trial that isolated it (Hall 2019, n=20, 2-week crossover) still found ~500 kcal/day higher intake on the ultra-processed arm at matched macronutrients. Default: use UPF share as a practical steering signal, not as a moral category.
- **Fish oil supplements for cardiovascular prevention.** Trials split by dose, formulation, and population, and the field is unsettled. Default: two portions of oily fish a week, supplements reserved for non-fish-eaters and for clinician-directed indications.
- **RDAs as individual targets.** An RDA is set to cover ~97.5% of a population, so it overshoots most individuals and undershoots a few; the EAR is the population-comparison figure. Use the RDA as a personal target and the trend in labs and symptoms as the correction — never as proof that an intake below it is a deficiency.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/nutrition (install if the user confirms):
- `calories` — calorie, macro, and weight-trend tracking, the energy half of the same diet
- `meal-planner` — turning the gaps found here into weekly menus and shopping lists
- `water` — fluid intake and electrolyte replacement
- `fitness` — training programs, and the nutrient demands they raise
- `fasting` — eating windows, and their effect on when nutrients can be taken

## Feedback

- If useful, star it: https://clawic.com/skills/nutrition
- Latest version: https://clawic.com/skills/nutrition

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/nutrition.
