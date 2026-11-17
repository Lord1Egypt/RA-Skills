# Supplements — Dose, Form, Timing, and When to Stop

A supplement is a targeted correction with a start date, a review date, and a stop rule. Everything else is a subscription. This file exists to make the four decisions in order: is there a gap, does food close it, what dose and form, and when does it end.

**Before proposing or reviewing anything**, read `## Supplements` in `~/Clawic/data/nutrition/memory.md` (or `supplements.md` if `## Boxes` points there) and the medications in `~/Clawic/data/health/profile.md`. The stack the user already has is where the UL gets crossed, and the medication list is where the timing collisions live (`interactions.md`).

**Contents:** [The Four Questions](#the-four-questions) · [Summing a Stack](#summing-a-stack) · [Forms That Differ](#forms-that-differ) · [Repletion Doses](#repletion-doses) · [Timing](#timing) · [Product Quality](#product-quality) · [Stop Rules](#stop-rules) · [Supplements With Little to Show](#supplements-with-little-to-show)

## The Four Questions

1. **Is there a gap?** Intake estimate or lab, never a symptom alone (SKILL.md Rule 4). No gap, no product.
2. **Does one realistic serving of food close ≥50% of it?** Then the food is the answer, and `supplement_posture` decides whether a supplement is offered alongside. The exceptions where food genuinely cannot: B12 on a vegan diet, vitamin D in winter above ~40°, iron repletion from a confirmed deficit, and clinician-directed doses.
3. **What dose, and does it fit under the ceiling?** `headroom = UL − (dietary intake + every other product containing it)`. Repletion doses that exceed the UL exist, but they are time-limited, clinician-directed, and stated as such.
4. **When does it stop or get reviewed?** A date, in `## Due`. Nutrients with a UL and no natural stop — iron, vitamin A, selenium, zinc, B6, niacin — get a stop rule, not just a review.

## Summing a Stack

The most common harm in this domain is not a bad supplement, it is three good ones that overlap. Sum before adding.

Worked example, a plausible stack:

| Product | Zinc | B6 | Vitamin A (preformed) | Iron |
|---|---|---|---|---|
| Multivitamin | 15 mg | 25 mg | 900 µg RAE | 18 mg |
| "Immune support" | 25 mg | — | — | — |
| B-complex | — | 50 mg | — | — |
| Diet | 10 mg | 2 mg | 600 µg RAE | 12 mg |
| **Total** | **50 mg** (UL 40) | **77 mg** (UL 100) | **1500 µg** (UL 3000) | **30 mg** (UL 45) |

Zinc is over the UL and heading for a copper deficiency; B6 is inside the UL but within reach of the neuropathy range if the user adds one more B-complex; iron is unneeded if no deficit was ever confirmed. The fix is subtraction — drop the multivitamin and the picture resolves. Any answer that adds a product without running this sum is guessing.

## Forms That Differ

Form matters when absorption, tolerance, or activity genuinely differ. Where it does not, the cheap form wins and saying so builds trust.

| Nutrient | Form that matters | Why |
|---|---|---|
| Iron | Ferrous bisglycinate or ferrous sulfate; state the **elemental** dose | 325 mg ferrous sulfate ≈ 65 mg elemental. Bisglycinate is gentler on the gut at similar elemental doses, which matters because GI intolerance is the main reason courses are abandoned |
| Calcium | Carbonate needs stomach acid, so it is taken with food and fails on PPIs; citrate absorbs without acid and is the post-bariatric and PPI form | Carbonate ~40% elemental by weight, citrate ~21% — the citrate pill is bigger for the same dose |
| Magnesium | Citrate, glycinate, malate absorb well; oxide is poorly absorbed and mostly a laxative | Oxide is not wrong if a laxative effect is the goal; it is wrong when repletion is |
| Vitamin D | D3 (cholecalciferol) over D2 (ergocalciferol) | D3 raises and holds 25-OH D more effectively; D2 is the vegetarian-labelled option, and vegan D3 from lichen exists |
| B12 | Cyanocobalamin works and is cheap; methylcobalamin is the marketed alternative with no clear advantage for ordinary use | Oral high-dose works even in pernicious anemia via passive absorption, but that case is clinician-managed |
| Folate | Folic acid is what the evidence for neural tube defect prevention used | 5-MTHF is sold for MTHFR variants; the practical case for switching is weak, and the fortification evidence rests on folic acid |
| Omega-3 | Triglyceride and re-esterified forms absorb somewhat better than ethyl esters; algal oil is the vegan source | Compare labels by **EPA+DHA content**, never by capsule size — a 1000 mg fish oil capsule often contains 300 mg EPA+DHA |
| Vitamin E | Natural d-alpha versus synthetic dl-alpha differ nearly 2× per IU | Convert to mg before comparing (`micronutrients.md`) |
| Iodine | Potassium iodide at a measured dose; kelp is unpredictable | Kelp products have exceeded the UL by an order of magnitude in testing |

## Repletion Doses

Above-RDA, time-limited, and only against a confirmed deficit. Below-RDA maintenance is a different conversation.

| Deficit | Typical repletion approach | Duration and end |
|---|---|---|
| Iron, confirmed low ferritin | 40-100 mg elemental daily-equivalent, given as a single dose on alternate days (Stoffel, Lancet Haematology 2017 — hepcidin stays raised ~24 h after a dose, so alternate-day gives higher fractional absorption) | Retest at 8-12 weeks; continue 3-6 months past hemoglobin normalizing; stop when ferritin is comfortably in range |
| Vitamin D, deficient | Clinician-directed loading regimens exist; a maintenance 1000-2000 IU/day suits most adults with insufficiency | Retest at ~3 months; annual or seasonal thereafter |
| B12, low with no neurological signs | Oral high-dose is effective for most causes | Retest at ~3 months. **Neurological signs mean clinician now, not a bigger tablet** (`safety.md`) |
| Folate, low | Standard supplemental doses correct it quickly | Establish B12 status **first** — folate corrects the blood picture while B12 nerve damage continues |
| Zinc, confirmed low | Short course with copper watched if it runs past a few weeks | Weeks, not months; sustained high zinc creates a copper problem |
| Magnesium | Split doses of a well-absorbed form; the GI limit arrives before the UL does | Symptom-driven; the target is dietary intake, not a permanent capsule |

Every repletion protocol goes to `artifacts/<nutrient>-repletion.md`, because it spans months and gets re-read at each retest (`memory-template.md`).

## Timing

| Take with | Nutrients | Reason |
|---|---|---|
| A fat-containing meal | A, D, E, K, omega-3 | Absorption depends on fat and bile in the same meal |
| Between meals or on an empty stomach | Iron (with vitamin C, away from tea, coffee, dairy, and calcium) | Food inhibitors cut absorption substantially; if the empty stomach is intolerable, a small non-dairy snack beats abandoning it |
| With food | Calcium carbonate, most B vitamins if nausea occurs | Carbonate needs acid; B vitamins on an empty stomach nauseate some people |
| Away from levothyroxine by 4 hours | Calcium, iron, magnesium | Direct binding; the separation is not optional (`interactions.md`) |
| Split across the day | Calcium above 500 mg, magnesium above the GI threshold | Per-dose absorption ceiling (SKILL.md Rule 6) |
| Morning | Anything with a stimulant, and B-complex for those who report sleep disturbance | Reported, not established — treat it as a tolerance preference: the timing note goes on that product's row in `## Supplements`, or in `config.yaml` if the user states it as a standing preference for every product |

Iron and calcium never share a dose. Zinc and copper compete, so a long zinc course is the one that needs copper watched. Two fat-soluble vitamins in the same meal is fine.

## Product Quality

Supplements are regulated as food, not as medicine, in most jurisdictions: content is the manufacturer's claim unless someone tested it.

- Prefer products carrying independent verification (USP, NSF, Informed Sport for athletes subject to testing). Contamination and mislabelling are documented and recurrent, especially in botanical and sports categories.
- Proprietary blends hide per-ingredient doses. A dose you cannot read cannot be summed against a UL, which makes the product unusable here.
- "Whole food" and "food-based" labels change the marketing, not the ceiling. The UL applies to the total from all sources.
- Herbal and botanical products are outside this skill's scope and belong in a clinician's interaction check: several have real drug interactions, St John's wort being the canonical one.
- Check the label for what else is in it — many single-nutrient products carry a second nutrient that lands in the sum above.

## Stop Rules

Written at the start, not decided later:

- **Repletion products** stop at the target lab value plus the specified store-filling period.
- **Seasonal products** stop on a date: vitamin D taken only from October to March, if that is the pattern chosen.
- **Trial products** get a defined window (typically 8-12 weeks) and an outcome that decides continuation. Write the outcome, whatever it is.
- **Anything with a UL** carries the sum from the stack table and a review each time a product is added.
- **A supplement whose reason cannot be stated** is stopped. If nobody can say what gap it closes, the gap is not there.

A stopped supplement keeps its row with the reason — that row is what stops it being restarted next January.

**Write in the same turn**: every start, dose change, form change, or stop into `## Supplements` in `~/Clawic/data/nutrition/memory.md`, with the elemental dose, the reason, the start date, and the review-or-stop rule; the review date into `## Due`; a multi-month repletion into `artifacts/` with its `## Boxes` line (`memory-template.md`). A stack that is not written down is re-summed from memory next time, and the memory is the user's.
