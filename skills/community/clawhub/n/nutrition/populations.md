# Populations — Life Stages That Change the Numbers

Requirements are not fixed. Pregnancy raises some by 50%, older age changes absorption rather than intake, and adolescence has the highest calcium and iron demands of any life stage. This file covers who needs different numbers and which ones move.

**Before applying any figure here**, read `## Life Stage`, the conditions, and the medications in `~/Clawic/data/health/profile.md`. Life stage is a health fact, not a preference: pregnancy, breastfeeding, and menopause go in the profile, never in `config.yaml`.

**Contents:** [Preconception and Pregnancy](#preconception-and-pregnancy) · [Breastfeeding](#breastfeeding) · [Infants and Young Children](#infants-and-young-children) · [Children and Adolescents](#children-and-adolescents) · [Older Adults](#older-adults) · [Menopause](#menopause) · [Athletes](#athletes) · [Vegan or Restricted Diets Within a Life Stage](#vegan-or-restricted-diets-within-a-life-stage)

## Preconception and Pregnancy

The stage with the highest stakes and the tightest timing. Everything here is advise-only alongside the clinician's prenatal care.

| Nutrient | Change | Detail |
|---|---|---|
| Folate | 600 µg DFE in pregnancy; **400 µg supplemental folic acid from preconception** | The neural tube closes by about week 4, before most pregnancies are confirmed — which is why the recommendation is aimed at anyone who could become pregnant, not at the confirmed pregnancy. Higher doses apply with a previous affected pregnancy or certain medications, set by a clinician |
| Iron | 27 mg | Plasma volume expands and requirements rise sharply in the second and third trimesters; pregnancy-specific hemoglobin and ferritin ranges apply (`labs.md`) |
| Iodine | 220 µg (290 breastfeeding) | Critical for fetal neurodevelopment, and frequently short where salt is not iodized |
| Choline | 450 mg | Consistently under-consumed and absent from many prenatal supplements — check the label |
| DHA | Commonly advised around 200-300 mg/day on top of general omega-3 intake | Algal oil where fish is not eaten |
| Calcium and vitamin D | Standard adult amounts, met reliably | Fetal demand is met from maternal bone if intake is short |
| **Preformed vitamin A** | **Ceiling, not a target: UL 3000 µg RAE** | Teratogenic in excess. Liver can exceed the UL in a single serving, and high-dose retinol supplements and retinoid medications are contraindicated |

Foods avoided in pregnancy, and the reason, because the reason determines the substitution:

- **High-mercury fish** — shark, swordfish, king mackerel, tilefish, bigeye tuna. Low-mercury fish is *encouraged*, not avoided: salmon, sardines, and light tuna within advised limits deliver the DHA.
- **Listeria risks** — unpasteurized dairy, soft mould-ripened cheese, deli meats unless heated, refrigerated pâté and smoked seafood.
- **Raw or undercooked** eggs, meat, and fish; unwashed produce (toxoplasma).
- **Alcohol** — no established safe amount.
- **Caffeine** — commonly limited to around 200 mg/day, which is roughly one to two cups of coffee depending on strength.
- **Liver and retinol supplements** — the vitamin A ceiling above.

Nausea and hyperemesis change everything: energy and fluid come first, prenatal vitamins may need a different timing or form, and severe cases carry a thiamin risk that is a clinician's concern.

## Breastfeeding

- Iodine rises to 290 µg — the highest requirement of any life stage — and B12 requirements rise with it. A vegan mother's B12 status determines the infant's, and infant B12 deficiency causes serious neurological harm.
- Energy and fluid needs rise; most other micronutrient requirements sit above pregnancy levels for the water-soluble vitamins because they pass into milk.
- Vitamin D in breast milk is low regardless of maternal status in most cases, which is why the infant gets drops rather than the mother getting more (below).
- Maternal deficiency shows in milk composition for the B vitamins, iodine, and vitamin A, and much less for calcium and iron, which are drawn from maternal stores instead.

## Infants and Young Children

Advise-only, alongside the pediatric clinician. Three rules with hard edges:

- **No honey before 12 months** — infant botulism risk.
- **Vitamin D drops for breastfed infants**, typically 400 IU/day, per the local pediatric guideline.
- **Iron from around 6 months**: stores laid down in utero deplete, and iron-rich complementary foods or fortified cereal are the standard answer. Cow's milk as a main drink before 12 months is associated with iron deficiency.
- Choking hazards and allergen introduction timing are pediatric guidance; current guidance in several countries favors *early* introduction of common allergens rather than delay, and the specifics belong to the clinician.
- Restrictive diets in infancy — including strict vegan without a supervised supplement plan — require clinical supervision, not this skill.

## Children and Adolescents

- Adolescence carries the peak lifetime requirements for calcium (1300 mg for ages 9-18) and, in menstruating adolescents, a high iron demand arriving at the same time as a growth spurt.
- Peak bone mass is largely accrued by the end of adolescence: calcium and vitamin D in these years are the deposit that osteoporosis prevention draws on decades later.
- Iron deficiency in adolescent girls is common and under-detected; fatigue in this group deserves a ferritin rather than a lecture about screens.
- **Never run restriction protocols, coverage scores, or elimination diets with a minor without clinician involvement** (`safety.md`). Growth is the priority over any optimization.
- Sports participation raises energy needs, and underfuelling in adolescent athletes is a recognized clinical problem (see Athletes).

## Older Adults

Absorption and appetite change more than the numbers do.

| Change | Why | What to do |
|---|---|---|
| B12 | Atrophic gastritis reduces the release of food-bound B12 in a substantial minority over 60 | Crystalline B12 from fortified foods or a supplement bypasses the acid step — recommended over "eat more meat" |
| Vitamin D | Skin synthesis declines with age; RDA rises to 800 IU at 71+ | Supplement, and pair with the falls conversation the clinician owns |
| Calcium | 1200 mg for women 51+ and everyone 71+ | Food first; split doses at 500 mg |
| Protein | Requirements are widely argued to be higher than the 0.8 g/kg RDA for preserving muscle | The quantitative target belongs to `calories` and `fitness`; the relevance here is that low intake worsens every other shortfall |
| Appetite and thirst | Both decline; medications and dental problems compound it | Nutrient density per bite becomes the design constraint, and fluid needs prompting (`water`) |
| Polypharmacy | The depletion list grows with the medication list | Run the interaction check as routine, not on suspicion (`interactions.md`) |

Unintentional weight loss in an older adult is a clinical red flag, not a nutrition win (`safety.md`).

## Menopause

- Bone loss accelerates in the years around the final period: calcium 1200 mg and adequate vitamin D become the baseline, with weight-bearing exercise doing the other half (`fitness`).
- Iron requirements **fall** to 8 mg after periods stop. Continuing a premenopausal-strength iron supplement out of habit is a common and avoidable overshoot — this is a stop-rule moment (`supplements.md`).
- Cardiovascular risk profile shifts, which raises the value of the fat-quality and sodium-potassium work in `diet-quality.md`.
- Body composition changes are a `calories` and `fitness` question; the nutrition side here is bone and cardiovascular.

## Athletes

The energy and macronutrient side belongs to `calories` and `fitness`. What changes here:

- **Iron**, especially in female endurance athletes: losses through sweat, gastrointestinal micro-bleeding, foot-strike hemolysis, and menstruation compound. Ferritin thresholds used in sports settings are typically higher than clinical anemia thresholds, and this is a genuine area of disagreement — say so, and work with the clinician's number.
- **Vitamin D** matters for bone and muscle function, and indoor and northern athletes are the ones who run short.
- **Calcium and energy availability**: low energy availability, whether deliberate or accidental, drives bone stress injuries and menstrual disruption. Relative Energy Deficiency in Sport (RED-S) is the umbrella term, and it is a clinician referral, not a supplement question (`safety.md`).
- **Sodium and fluid** in heavy sweating belong to `water`.
- **Supplement contamination** is a career risk for tested athletes: third-party certification (Informed Sport and equivalents) is the requirement, not a nicety (`supplements.md`).
- Antioxidant mega-doses around training have been reported to blunt some training adaptations; food-level intake is not implicated, high-dose supplements are.

## Vegan or Restricted Diets Within a Life Stage

Stacking a pattern on a life stage compounds both lists and is where the real risk sits:

- **Vegan pregnancy or breastfeeding**: B12, iodine, DHA, iron, choline, and vitamin D all at once — supervised, supplemented, and monitored, not improvised.
- **Vegan infants and children**: supervised by a pediatric clinician. B12 deficiency in a breastfed infant of a B12-deficient mother is a documented and serious harm.
- **Older adult on a restricted diet**: reduced absorption plus reduced intake, with protein and B12 leading the list.
- **Adolescent adopting a restrictive diet**: run the eating-disorder screen before the nutrition advice. A new restriction in a teenager is sometimes the presenting sign, not the topic (`safety.md`).

**Write in the same turn**: the life stage and its start date into `## Life Stage` of `~/Clawic/data/health/profile.md`; the changed requirements into `## Nutrient Status` with the life stage as the evidence; stage-driven dates — trimester reviews, the postpartum iron recheck, the menopause iron stop — into `## Due` (`memory-template.md`). Life stages expire, and an expired requirement left in place is how a postmenopausal woman keeps taking 18 mg of iron.
