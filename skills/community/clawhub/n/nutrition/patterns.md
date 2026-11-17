# Diet Patterns — Their Gaps and Their Fixes

Every pattern has a predictable gap list. That is the useful fact here: the gaps can be closed the day the pattern starts, without waiting for a symptom or a lab. Set `diet_pattern` and the coverage check runs the right list by default.

**Before running a pattern's gap list**, read `## Nutrient Status` in `~/Clawic/data/nutrition/memory.md` and the conditions and medications in `~/Clawic/data/health/profile.md`. A pattern layered on a condition (keto with kidney disease, low-FODMAP on top of dairy-free) produces a different list than either alone.

**Contents:** [Vegan](#vegan) · [Vegetarian and Pescatarian](#vegetarian-and-pescatarian) · [Keto and Very-Low-Carb](#keto-and-very-low-carb) · [Gluten-Free](#gluten-free) · [Mediterranean](#mediterranean) · [DASH](#dash) · [Low-FODMAP](#low-fodmap) · [Paleo and Whole-Food Exclusion Diets](#paleo-and-whole-food-exclusion-diets) · [Religious and Cultural Patterns](#religious-and-cultural-patterns) · [Switching Patterns](#switching-patterns)

## Vegan

The most predictable gap list in nutrition, and the easiest to close deliberately.

| Nutrient | Why | Fix |
|---|---|---|
| **B12** | No reliable unfortified plant source. Spirulina and nori carry inactive analogues that can make the picture look better than it is | A supplement, not a hope. Fortified foods work only with three reliable servings a day |
| Iron | Non-heme only, at 2-20% absorption against 15-35% for heme | Vitamin C in the same meal, tea and coffee moved an hour away (`absorption.md`); ferritin rather than assumption |
| Iodine | Dairy and fish are the usual sources; seaweed is wildly variable and can overshoot the UL | Iodized salt at a measured amount, or a supplement at 150 µg |
| Omega-3 EPA/DHA | ALA converts at ~5-8% to EPA and well under 1% to DHA | Algal oil, 250-500 mg EPA+DHA |
| Vitamin D | Few plant sources; D3 from lichen exists for those avoiding lanolin-derived D3 | Supplement in winter above ~40° latitude regardless of pattern |
| Calcium | Dairy removed; spinach's calcium is oxalate-bound at ~5% absorption | Calcium-set tofu, fortified plant milk (check the label — not all are), low-oxalate greens |
| Zinc | Phytate-bound; vegetarian requirements run up to ~50% higher | Soaked and fermented legumes and grains, pumpkin seeds |
| Choline | Eggs are the dominant source | Soy, cruciferous vegetables, quinoa; often still short |
| Protein quality | Adequate on a varied diet; lysine is the limiting amino acid in grain-heavy patterns | Legumes daily. Combining at every meal is unnecessary; variety across the day suffices |

Selenium is soil-dependent and worth a look in low-selenium regions. B12 status is the one that gets an annual check rather than a guess (`labs.md`).

## Vegetarian and Pescatarian

- **Lacto-ovo vegetarian**: B12 and iodine come with dairy and eggs, so the live gaps narrow to iron, zinc, and omega-3 EPA/DHA. Choline is fine if eggs are eaten.
- **Pescatarian**: essentially covered. Omega-3, B12, iodine, and selenium all arrive with fish; iron remains the one to watch in menstruating women.
- The common failure is a **"vegetarian" diet that is mostly refined carbohydrate** — pasta, bread, cheese. It carries every gap of a vegan diet except B12, plus a fiber and potassium shortfall. Check what is actually eaten, not the label the person uses.
- Vegetarian iron requirements are conventionally estimated as higher than omnivore requirements because of lower bioavailability; use the higher target and confirm with ferritin rather than arguing the multiplier.

## Keto and Very-Low-Carb

| Nutrient | Why | Fix |
|---|---|---|
| Fiber | Grains, legumes, and most fruit are out; this is the largest and most consistent shortfall | Avocado, chia, flax, nuts, non-starchy vegetables in volume; a psyllium supplement if it still falls short |
| Potassium and magnesium | Low intake plus the early diuresis of carbohydrate restriction — the source of "keto flu" cramps and fatigue | Avocado, nuts, seeds, leafy greens; sodium is usually raised deliberately in the first weeks |
| Thiamin, folate, vitamin C | Fortified grains and fruit removed | Vegetables, and check the diet is not meat-and-cheese only |
| Calcium | Depends entirely on whether dairy is in | Dairy or fortified alternatives |
| Microbiome substrate | Fermentable fiber drops sharply | Non-starchy vegetable variety; the plant-count target still applies |

Keto is a therapeutic diet with an established indication in refractory epilepsy and a broader popular use. It is a clinician's diet in type 1 diabetes, on SGLT2 inhibitors (ketoacidosis risk), in pregnancy, and in kidney or liver disease. Long-term lipid changes vary widely between individuals and are worth monitoring.

## Gluten-Free

Two populations, and they need different answers. **Celiac disease** is a medical necessity with strict cross-contamination rules (`restrictions.md`, `conditions.md`). **Non-celiac choice** is a preference — and often the outcome of an untested self-diagnosis.

- **Screen for celiac before removing gluten.** The test requires gluten in the diet; removing it first means a diagnostic gap that takes a supervised gluten challenge to close.
- Nutrient cost: most gluten-free flours are unfortified where wheat flour is fortified, so fiber, folate, iron, and B vitamins all drop. In folic-acid-fortifying countries this matters most for women who might become pregnant.
- Fixes: oats certified gluten-free where tolerated, buckwheat, quinoa, teff, legumes, and brown rice over white rice flour products. Naturally gluten-free whole foods beat gluten-free replicas of bread and cake, which are usually lower in fiber and higher in fat and sugar.
- Arsenic in rice is worth a mention for diets that lean heavily on rice-based gluten-free products: vary the grain rather than eliminating rice.

## Mediterranean

The pattern with the strongest cardiovascular evidence base, and the one people implement as "olive oil and pasta".

- Components that matter: olive oil as the primary fat, legumes and whole grains daily, fish weekly, nuts daily, vegetables and fruit in volume, moderate dairy mostly as yogurt and cheese, low red and processed meat.
- Evidence: PREDIMED reported a substantial reduction in major cardiovascular events with olive-oil- and nut-supplemented Mediterranean diets. The trial was retracted and republished in 2018 after randomization irregularities were found at some sites; the republished analysis retained the direction and magnitude. Say the caveat when citing it.
- Gaps: essentially none if implemented fully. Iron in menstruating women and vitamin D by latitude remain, as they do on any pattern.
- The common failure is adopting the pleasant half (bread, pasta, cheese, wine) without the legumes, fish, and vegetable volume that carry the effect.

## DASH

- Designed for blood pressure: high fruit, vegetables, low-fat dairy, whole grains, nuts; low sodium, red meat, and sweets.
- Trial effect: roughly 5-6 mmHg systolic in the original DASH trial, larger in hypertensive participants, and larger again with the low-sodium arm.
- Its real mechanism overlaps this skill's Rule 9 — it raises potassium, calcium, and magnesium while lowering sodium, which is the ratio argument in a branded package.
- Gaps: none inherent. The obstacle is sodium, since ~70% of intake is in processed and restaurant food (`diet-quality.md`).
- **Not for CKD without clinician direction**: the potassium load that makes DASH work is the thing being restricted (`conditions.md`).

## Low-FODMAP

A three-phase diagnostic protocol, not a long-term diet — full protocol in `gut.md`. Gaps arise entirely from staying in phase 1: fiber, calcium if dairy is out, prebiotic substrate, and some B vitamins. The instruction that matters is that reintroduction is mandatory and scheduled.

## Paleo and Whole-Food Exclusion Diets

- Excludes grains, legumes, and usually dairy. The gaps follow directly: calcium and vitamin D (no dairy), fiber and folate (no grains or legumes), and iodine if dairy was the source.
- The quality upside is real — high vegetable intake, minimal ultra-processed food — and it is worth saying so rather than arguing the anthropology.
- Fixes: canned fish with bones, calcium-set alternatives, high vegetable and nut volume for fiber and magnesium, iodized salt.
- The same analysis applies to any self-designed exclusion diet: list what left, close what it carried, and keep what the pattern does well.

## Religious and Cultural Patterns

- **Halal and kosher**: no inherent nutrient gaps; the practical questions are gelatin, enzymes, and additives in supplements. Vegetarian or fish-derived capsule sources exist and are worth naming, since a supplement recommendation that cannot be taken is not a recommendation.
- **Ramadan and other fasting observances**: the nutrient question is fitting the day's requirements into the eating window, and hydration. Timing of iron and calcium around the two meals matters more than usual (`interactions.md`); fasting mechanics belong to `fasting`.
- **Lent, Ekadashi, and other periodic restrictions**: short enough that only B12 and iron matter, and only if the pattern is frequent.
- **Regional staple patterns** shape both gaps and fixes. Ask what the household actually cooks before recommending foods that will not be bought, and record it in `## Usual Foods`.

## Switching Patterns

A pattern change is the highest-yield moment in this whole skill, because the gaps are predictable before they appear:

1. List what left the diet and what each removed food was carrying.
2. Name the replacement for each nutrient, with the serving size, on day one.
3. Set the baseline labs worth having if the pattern is long-term: B12 and ferritin for a new vegan, 25-OH D for anyone in winter.
4. Put the first review in `## Due` at 3 months, and the B12 check at 12.
5. Update `diet_pattern` in `config.yaml` — it is a declared preference, and it changes the default gap list from then on.

**Write in the same turn**: the new `diet_pattern` into `config.yaml`; the pattern's gap list into `## Nutrient Status` with status `watch` and the pattern named as the evidence; the review and lab dates into `## Due`; a transition worth re-reading into `artifacts/<pattern>-transition.md` with its `## Boxes` line (`memory-template.md`). A gap list written on day one is what makes month six uneventful.
