# Absorption — Why Intake and Blood Levels Disagree

The label states what went in the mouth. Blood reflects what crossed the gut wall, and for iron, calcium, zinc, and the carotenoids the difference is several-fold. This file is for the situation "I eat plenty of it and the number stays low" — and for making a modest intake work harder than a large one.

**Before rewriting someone's diet upward**, read `## Usual Foods` in `~/Clawic/data/nutrition/memory.md` (or `foods.md` if `## Boxes` points there) and the conditions in `~/Clawic/data/health/profile.md`. Malabsorption changes the answer completely (`conditions.md`), and the fix is usually a pairing change inside meals the user already eats.

**Contents:** [Absorption Rates Worth Knowing](#absorption-rates-worth-knowing) · [Enhancers](#enhancers) · [Inhibitors](#inhibitors) · [Meal Engineering](#meal-engineering) · [Cooking and Preparation](#cooking-and-preparation) · [Storage Losses](#storage-losses) · [Dose Ceilings](#dose-ceilings) · [When Absorption Is Not the Problem](#when-absorption-is-not-the-problem)

## Absorption Rates Worth Knowing

Ranges, because the meal around the nutrient moves them.

| Nutrient | Typical absorbed fraction | What moves it |
|---|---|---|
| Heme iron (meat, fish, poultry) | ~15-35% | Little — this is the point of heme iron |
| Non-heme iron (plants, supplements, fortificants) | ~2-20% | Vitamin C up, phytate/tannin/calcium down, body stores up when depleted |
| Calcium from dairy | ~30% | Vitamin D status; per-dose ceiling |
| Calcium from low-oxalate greens (kale, bok choy) | ~50% | The highest fractional absorption of any common source, though the per-serving amount is small |
| Calcium from spinach | ~5% | Oxalate binds it; the label figure is nearly irrelevant |
| Zinc | ~15-35% | Phytate is the dominant inhibitor; vegetarian requirements run up to ~50% higher |
| Beta-carotene | Low and highly variable | Fat in the meal, cooking, and the food matrix all raise it |
| Folate as folic acid | Higher than food folate | 1 µg folic acid with food ≈ 1.7 µg DFE |
| B12, food-bound | Requires stomach acid and intrinsic factor | Fails with atrophic gastritis and PPIs; crystalline B12 in fortified food and supplements bypasses the acid step |
| Magnesium, supplemental | Form-dependent; oxide poorly | Citrate, glycinate, malate absorb far better than oxide |

## Enhancers

| Enhancer | Raises | How to use it |
|---|---|---|
| Vitamin C in the same meal | Non-heme iron, substantially | 50-100 mg — a pepper, a citrus fruit, a tomato sauce. It works only in the same meal, not as a separate tablet later |
| Meat, fish, poultry in the meal | Non-heme iron | The "meat factor" raises absorption from plant foods eaten alongside |
| Dietary fat | A, D, E, K, carotenoids, lycopene | A carotene-rich salad with no fat delivers a fraction of what it appears to; olive oil or avocado in the same dish fixes it |
| Fermentation, soaking, sprouting | Iron, zinc, magnesium | Degrades phytate. Sourdough leavening is the practical example; overnight-soaked and drained legumes the other |
| Cooking, for some carotenoids | Lycopene, beta-carotene | Heat breaks the matrix — cooked tomato beats raw for lycopene |
| Vitamin D status | Calcium | Adequate D is a prerequisite for the 30% figure above |
| Depleted stores | Iron | The body raises fractional absorption when ferritin is low, which is why repletion works faster than the arithmetic suggests |

## Inhibitors

| Inhibitor | Reduces | Practical rule |
|---|---|---|
| Phytate (whole grains, legumes, nuts, seeds) | Iron, zinc, calcium, magnesium | Soak, sprout, or ferment; do not abandon the food — it is the same food carrying the nutrient |
| Oxalate (spinach, chard, beet greens, rhubarb) | Calcium, iron | Choose low-oxalate greens for minerals; spinach remains a fine food for folate and potassium |
| Tannins and polyphenols (tea, coffee, red wine, cocoa) | Non-heme iron, strongly | Move tea and coffee ≥1 hour from an iron-focused meal or supplement. This single change often outperforms adding iron |
| Calcium | Iron, both heme and non-heme | Separate the calcium supplement and the dairy course from the iron meal by ≥2 hours |
| Zinc at supplement doses | Copper, iron | Cap and separate (`interactions.md`) |
| Fiber, very high and abrupt | Minerals, modestly | Real but overstated; the ramp protocol matters more (`gut.md`) |
| Low stomach acid (PPIs, atrophic gastritis, post-bariatric) | B12, iron, calcium carbonate, magnesium | Switch calcium to citrate, expect B12 monitoring, and read the condition file (`conditions.md`) |
| Alcohol | Thiamin, folate, B12, zinc, magnesium | Both absorption and retention are affected |

## Meal Engineering

The whole file compressed into what changes on a plate. Each of these moves a real number without changing what the person eats.

- **Lentils with a squeeze of lemon and peppers, tea an hour later** rather than lentils with tea — the same iron, a much larger absorbed fraction.
- **Coffee moved out of the iron-supplement window**: alternate-day iron on waking with juice, coffee after 10 a.m.
- **Yogurt at a different meal from the beans**, when iron is the target and calcium is high.
- **Oil on the carrots and the tomato sauce**, always: fat-free carotenoid meals are the quiet waste in "healthy" eating.
- **Sourdough or soaked legumes** where whole grains and pulses form the bulk of the diet: phytate reduction is worth more than a supplement here.
- **Calcium split at 500 mg** and taken away from the iron meal (SKILL.md Rule 6).
- **Fortified foods for B12 spread across the day**: the passive-absorption pathway is dose-limited, so three small exposures beat one large one for food sources.

## Cooking and Preparation

| Method | Effect | Which nutrients |
|---|---|---|
| Boiling in water then draining | Largest routine loss — nutrients leave into the water | Vitamin C, folate, B vitamins, potassium |
| Steaming, microwaving, pressure cooking | Much smaller losses; short times and little water | Same group |
| Roasting and grilling | Moderate loss of heat-labile vitamins, no leaching | Vitamin C, thiamin |
| Cooking with the water retained (soups, stews) | Losses stay in the dish | Everything water-soluble |
| Cutting and then storing | Increases surface oxidation | Vitamin C, folate |
| Cooking tomatoes and carrots | Increases available lycopene and beta-carotene | Carotenoids |
| Prolonged reheating | Cumulative loss with each cycle | Vitamin C, folate |

Minerals do not degrade with heat — they only leach. If the cooking water goes into the dish, the minerals do too.

## Storage Losses

- Fresh produce loses vitamin C and folate steadily from harvest; a week-old spinach is not the food the database describes.
- **Frozen at harvest often beats "fresh" that travelled and sat** — this is the counterintuitive one worth telling people, and it makes the cheaper option the better one.
- Light degrades riboflavin (the reason for opaque milk containers) and vitamin A.
- Cut surfaces, warmth, and air are the three accelerants; whole and cold is the storage rule.
- Canning costs heat-labile vitamins but preserves minerals and, for fish with bones, delivers calcium that fresh fillets do not.

## Dose Ceilings

Absorption is saturable, so a large single dose is not proportionally more nutrient.

- Calcium: ≤500 mg per dose (`supplements.md`).
- Iron: hepcidin rises for roughly 24 hours after a dose, which is the basis of alternate-day dosing (Stoffel, Lancet Haematology 2017).
- Magnesium: the practical ceiling is GI tolerance, and it arrives before the UL.
- Vitamin C: fractional absorption falls as the dose rises; grams give diminishing returns and GI symptoms.
- Water-soluble vitamins in general: excess is excreted, which is why a mega-dose multivitamin produces bright urine and no benefit.

## When Absorption Is Not the Problem

Do not spend a session on pairings when one of these is present:

- **Ongoing losses** — heavy menstrual bleeding, GI bleeding, frequent donation. No absorption fix outpaces the loss; find the loss.
- **A malabsorptive condition** — celiac, IBD, pancreatic insufficiency, post-bariatric anatomy. The condition is the answer (`conditions.md`).
- **A dose that was never adequate** — check the arithmetic before blaming absorption.
- **The wrong marker** — a normal-range ferritin with high CRP was never a real reading (`labs.md`).
- **Non-adherence** — the most common reason a supplement did not work is that it was not taken, and GI intolerance is why. A gentler form at a lower frequency beats a perfect regimen abandoned in week two.

**Write in the same turn**: a pairing or timing change that worked into the food's row in `## Usual Foods`, and into the relevant `## Supplements` row as its timing note; a meal-level fix worth reusing into the nutrient's `## Nutrient Status` evidence column (`memory-template.md`). "Take the iron away from tea" is exactly the instruction that gets forgotten and re-derived three months later.
