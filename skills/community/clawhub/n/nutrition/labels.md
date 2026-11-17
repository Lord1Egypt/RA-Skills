# Labels — Reading a Package for Nutrients

A nutrition panel answers a different question depending on which country printed it. This file covers the arithmetic that makes a label usable, the claims that mean less than they appear, and the ingredient-list reading that finds what the panel omits.

**Before adding a food to the user's rotation**, read `## Usual Foods` in `~/Clawic/data/nutrition/memory.md` (or `foods.md` if `## Boxes` points there) — a food already profiled does not get re-derived, and re-derivation is how two different numbers for the same yogurt end up in the record. `reference_standard` decides whether %DV or %NRV applies.

**Contents:** [The Serving-Size Audit](#the-serving-size-audit) · [Percent Daily Value and NRV](#percent-daily-value-and-nrv) · [US Versus EU Panels](#us-versus-eu-panels) · [The Ingredient List](#the-ingredient-list) · [Claims and What They Mean](#claims-and-what-they-mean) · [Fortification](#fortification) · [Supplement Labels](#supplement-labels) · [Rounding and Tolerance](#rounding-and-tolerance)

## The Serving-Size Audit

Always the first step, because every other number on the panel is downstream of it.

1. **Read the serving size and the servings per container** before any nutrient figure.
2. **Compute what will actually be eaten.** A 500 ml bottle labelled "2.5 servings" is one drink for most people; multiply everything by 2.5.
3. **Check the basis**: dry versus cooked, drained versus in liquid, with or without the packaging medium. Dry pasta at ~350 kcal/100 g and cooked pasta at ~130 kcal/100 g is the same food and a 2.7× arithmetic error.
4. **Convert to the comparison unit.** Per-100 g figures compare products; per-serving figures compute a day. Doing both prevents the classic mistake of comparing a per-serving figure against a per-100 g one.
5. **Cross-check against reality**: weigh the portion once. One weighing calibrates the eye for a food that recurs weekly.

## Percent Daily Value and NRV

- **US %DV** is the percentage of a fixed reference intake for a 2000 kcal diet — **not** of the individual's requirement. For a nutrient whose RDA differs by sex or life stage (iron, calcium, folate), the %DV can be substantially wrong for the person reading it.
- **EU %NRV** works the same way against the EU's reference values, which differ from the US ones for several nutrients.
- Rules of thumb baked into US labelling: **≤5% DV is low, ≥20% DV is high** in a serving. Useful for scanning a shelf, useless for computing a day.
- To convert back to an amount: `amount = %DV × reference value ÷ 100`. Calcium at 20% DV against a 1300 mg reference is 260 mg, and if the reader needs 1200 mg the coverage is different again.
- Micronutrients on the US panel are limited to vitamin D, calcium, iron, and potassium as mandatory since the 2016 label update; magnesium, zinc, B12, and the rest appear only voluntarily or when a claim is made. **A nutrient's absence from the panel says nothing about its presence in the food.**

## US Versus EU Panels

| Element | US | EU |
|---|---|---|
| Basis | Per serving, with per-container where relevant | Per 100 g or 100 ml mandatory, per portion optional |
| Sodium | Sodium in mg | **Salt in g** — salt g × 400 = sodium mg |
| Sugars | Total sugars and **added sugars** separately | Total sugars only; added sugar must be inferred from the ingredient list |
| Energy | kcal | kJ and kcal (kcal = kJ ÷ 4.184) |
| Micronutrients | Vitamin D, calcium, iron, potassium mandatory | Only when a claim is made or fortification occurred |
| Allergens | 9 major allergens declared | 14 declared, **emphasized in the ingredient list** (bold or capitals) rather than in a separate statement |
| Fiber | "Dietary fiber", with a US-specific definition of what counts | "Fibre", with a different analytical definition — figures are not strictly comparable across systems |

A user who shops in both systems is reading two different documents, and the sodium-versus-salt conversion is the one that silently doubles or halves a number.

## The Ingredient List

Where the panel's omissions live. Ordered by weight, descending.

- **Sugar fragmentation**: five sweeteners each appearing separately keep any one of them out of the top three. Anything ending in -ose, syrups, concentrates, malt, molasses, honey, agave, fruit juice concentrate. Add them mentally.
- **Fat quality**: "vegetable oil" without naming the oil, palm oil, hydrogenated or partially hydrogenated fats.
- **Sodium sources beyond salt**: sodium benzoate, monosodium glutamate, sodium nitrite, sodium phosphate, baking soda.
- **Phosphate additives**: any "phos-" compound. Nearly completely absorbed, unlike organic phosphorus in whole foods — the distinction that matters in kidney disease (`conditions.md`).
- **Allergen hiding places**: whey and casein for milk, albumin and lysozyme for egg, lecithin for soy, malt for barley (`restrictions.md`).
- **Sugar alcohols**: any -itol. Above roughly 10-20 g they cause GI symptoms, and they are the frequent unexplained cause of bloating (`gut.md`).
- **Fortificants** appear here even when the panel does not list them: "ferrous fumarate", "folic acid", "cyanocobalamin", "calcium carbonate".
- **Length as a signal**: a long list of substances not found in a kitchen is the practical NOVA group 4 test (`diet-quality.md`).

## Claims and What They Mean

| Claim | The regulated meaning | The reading |
|---|---|---|
| "No added sugar" | No sugar added during processing | The food may be high in intrinsic sugar — fruit juice qualifies |
| "Reduced" X | Typically a set percentage less than the reference product | Reduced from a high baseline can still be high |
| "Light" or "lite" | Reduced energy or fat against a reference, in regulated systems; in others it can refer to color or texture | Read the panel |
| "High in fiber" / "source of fiber" | Threshold-based per 100 g in the EU; US uses %DV thresholds | The claim is true and can coexist with high sugar |
| "Natural" | Weakly regulated to unregulated depending on jurisdiction | No nutritional meaning |
| "Multigrain" | Contains more than one grain | Says nothing about whole grain |
| "Whole grain" as the first ingredient | Meaningful | The reliable whole-grain signal |
| "Fortified" or "enriched" | Nutrients added, or restored after processing | Check which, and at what amount — it appears in the ingredient list |
| "Plant-based" | Marketing | Ultra-processed plant-based products are still ultra-processed |
| "Keto", "paleo", "clean" | Unregulated | Ignore and read the panel |
| Front-of-pack scores (Nutri-Score, traffic lights, health stars) | Algorithmic summaries of the panel | Useful for comparing two products in the same category, poor across categories |

## Fortification

What is fortified varies by country, which is why `platform.country` changes the baseline before anyone changes their diet.

- **Folic acid in flour**: mandatory in the US, Canada, and many other countries; absent in most of the EU. This single difference changes folate adequacy at a population level and matters most for preconception.
- **Iodized salt**: mandatory in some countries, voluntary in others, and absent from most sea, kosher, and specialty salts everywhere.
- **Vitamin D**: fortified milk is standard in the US, patchy in Europe.
- **Plant milks**: fortification with calcium, B12, and vitamin D is voluntary and inconsistent. **Check the label of the specific product** — organic ranges are frequently unfortified, and an unfortified plant milk substituted for dairy removes calcium, iodine, and B12 at once.
- **Breakfast cereals** are often the largest single fortificant source in a diet, which cuts both ways: they close gaps, and they are also where a stack quietly gains another 100% DV of several nutrients.

## Supplement Labels

- **Elemental amount is the number that matters**: 325 mg ferrous sulfate is ~65 mg elemental iron; 500 mg calcium carbonate is ~200 mg elemental calcium. Record the elemental figure in the product's `## Supplements` row (`supplements.md`).
- **%DV over 100%** is common and legal, and is where a stack's total climbs. Sum across all products against the UL (SKILL.md Rule 3).
- **Proprietary blends** hide per-ingredient doses; a dose that cannot be read cannot be summed, which makes the product unusable for planning.
- **Serving size on a supplement is often 2-3 capsules** — the panel's figures are per serving, not per capsule, and this is a routine source of dosing error in both directions.
- **Third-party verification marks** (USP, NSF, Informed Sport) indicate content testing. Supplements are regulated as food in most jurisdictions, so unverified content is a claim.
- **"Other ingredients"** carries the allergens and excipients: lactose, gelatin, soy, wheat starch.
- Expiry dates matter more for some nutrients than others; potency declines over time, and a half-used bottle from three years ago is not delivering its label.

## Rounding and Tolerance

- Panel values are rounded, and small amounts can round to zero — a "0 g trans fat" claim can sit on a genuinely non-zero amount per serving under some rounding rules, which is why the ingredient list's "partially hydrogenated" matters more than the panel figure.
- Analytical tolerances mean the printed figure is a permitted approximation of the tested content, not a measurement of the package in hand.
- Natural variation in whole foods is larger than any of this: the selenium in a Brazil nut varies with the soil it grew in, and the vitamin D in a mushroom depends on its UV exposure.
- Practical consequence: treat label micronutrient figures as good estimates, and reserve precision for the decisions that need it — a UL sum, or a prescribed dose.

**Write in the same turn**: a food whose nutrient profile was worked out into `## Usual Foods` with the serving size and what that serving delivers; a fortification fact about the user's country into `config.yaml` under `platform`; a product-level finding worth remembering — an unfortified plant milk, a supplement's real elemental dose — into the relevant `## Usual Foods` or `## Supplements` row (`memory-template.md`). The point of the food library is that the panel is read once.
