# Restrictions — Allergy, Intolerance, and Structured Elimination

Three different things get called "I can't eat that": an immune allergy, an enzymatic or functional intolerance, and a dislike or belief. They need different handling, different safety margins, and different nutrient replacements.

**Before any elimination or any food recommendation**, read the allergies and intolerances in `~/Clawic/data/health/profile.md` and the history in `## Reactions` of `~/Clawic/data/nutrition/memory.md` (or `reactions.md` if `## Boxes` points there). This is the read that prevents the worst mistake this skill can make.

**Contents:** [Telling Them Apart](#telling-them-apart) · [Allergy Handling](#allergy-handling) · [Intolerances](#intolerances) · [The Elimination Protocol](#the-elimination-protocol) · [Reintroduction](#reintroduction) · [Replacing What Was Removed](#replacing-what-was-removed) · [Hidden Sources](#hidden-sources) · [Tests That Do Not Work](#tests-that-do-not-work)

## Telling Them Apart

| | Allergy | Intolerance | Avoidance by choice |
|---|---|---|---|
| Mechanism | Immune, usually IgE | Enzymatic, malabsorptive, or functional | Preference, ethics, belief |
| Onset | Minutes to ~2 hours | 30 minutes to many hours, often dose-related | — |
| Dose | Trace amounts can trigger | Threshold effect — a small amount is often fine | — |
| Symptoms | Hives, swelling, airway, vomiting, anaphylaxis | GI symptoms, headaches, malaise | — |
| Confirmed by | Allergist: history plus skin prick or specific IgE, sometimes a supervised challenge | Structured elimination and reintroduction, breath tests for lactose or fructose | Nothing to confirm |
| Where it is stored | `health/profile.md`, Allergies table | `health/profile.md`, Allergies table, typed as intolerance | `config.yaml` under restrictions |
| Margin | Zero. Cross-contamination counts | Threshold, personal and testable | None needed |

The storage split matters: a choice recorded as an allergy makes every future recommendation more restrictive than it needs to be, and an allergy recorded as a preference is a safety failure.

## Allergy Handling

- **No dose reasoning, ever.** With an allergy the answer is not "a little is fine". Cross-contamination on shared equipment is a real exposure route, and "may contain" labelling exists because of it.
- The major allergen groups are declared on labels in most jurisdictions, though the lists differ: the EU declares 14 including celery, mustard, lupin, sulphites, and molluscs; the US declares 9, sesame having been added in 2023. A user shopping across both systems is reading two different label rules (`labels.md`).
- Precautionary "may contain" statements are voluntary in many places and their absence is not a guarantee — say that plainly rather than implying a clean label is a clean product.
- Anaphylaxis history means an emergency plan exists and belongs with the clinician, not here. This skill's job is the nutrient replacement and the label literacy.
- Alpha-gal syndrome (delayed mammalian meat allergy after certain tick bites) is worth knowing because the delayed onset — often 3-6 hours — makes it invisible to ordinary food-symptom logging.
- Oral allergy syndrome (pollen-food cross-reactivity: raw apple with birch pollen, melon with ragweed) usually spares cooked forms, which preserves most of the nutrition. It is not the same as a primary food allergy and is worth distinguishing.

## Intolerances

| Intolerance | Mechanism | Threshold behavior | Practical handling |
|---|---|---|---|
| Lactose | Lactase decline after weaning; prevalence varies enormously by ancestry | Most people with it tolerate ~12 g at once (about 240 ml milk), more when spread out or taken with a meal | Keep hard cheese (near-zero lactose) and yogurt (bacterial lactase); use lactase enzyme or lactose-free milk. **A full dairy exclusion is almost never necessary and costs ~600 mg calcium a day** |
| Fructose malabsorption | Limited intestinal transport capacity | Dose-dependent, and better tolerated when glucose is present in the food | Overlaps FODMAP handling (`gut.md`) |
| Histamine intolerance | Contested mechanism, poor diagnostic tests | Reported as cumulative across a day | Handle as a symptom-logged trial with a defined endpoint, not as an indefinite diet |
| Sulphites | Sensitivity, notably in some asthmatics | Dose-related | Declared on EU labels above 10 mg/kg |
| Caffeine | Metabolic rate varies genetically | Highly individual | Timing and total dose; not a nutrient question |
| Sugar alcohols | Osmotic and fermentative | Symptoms common above ~10-20 g | Read for -itol endings; frequently the entire explanation for unexplained bloating |
| Gluten, non-celiac | Contested; fructans in wheat may explain part of it | Variable | **Celiac screen first, while gluten is still in the diet** (`conditions.md`) |

## The Elimination Protocol

Only when a suspicion exists and testing has not answered it. It has an end date by design.

1. **Screen first.** Celiac serology before removing wheat; an allergist referral before removing a suspected allergen from a child's diet. Removing the food first destroys the test.
2. **One food or group at a time.** Simultaneous eliminations produce an unattributable result and a diet nobody can rebuild.
3. **2-4 weeks, with an end date written down.** Longer rarely adds information and starts costing nutrients and social eating.
4. **Replace what leaves on day one** — see the table below. The skipped replacement is what turns a two-week diagnostic into a three-month deficiency.
5. **Log daily** in `## Reactions`: the food, the amount, the symptom, and the onset time. Also log the non-food variables — sleep, stress, cycle phase, alcohol — because they move the same symptoms.
6. **Set the reintroduction date in `## Due` at the start**, not when the elimination ends. Eliminations without a scheduled end become permanent by drift.
7. **Not for children without clinician supervision**, and not for anyone with an eating-disorder history (`safety.md`).

## Reintroduction

The half that produces the answer, and the half that gets skipped.

- Reintroduce **one food at a time**, in a normal portion, with 72 hours before the next one. Delayed reactions are why 72 hours and not 24.
- Start with the form most likely to be tolerated, then escalate: hard cheese → yogurt → milk for dairy; cooked → raw for oral allergy syndrome patterns.
- A negative reintroduction is a **result**: the food goes back in the diet, and it goes back into `## Usual Foods`. Restoring a food is as valuable as removing one, and it is the outcome most people never get.
- A positive reintroduction gets a threshold test, not a ban: how much, how often, and with what else. Threshold behavior is the defining feature of intolerance.
- Record the outcome in the elimination artifact and update `health/profile.md`. An intolerance confirmed by trial gets its `Confirmed by` column filled with the trial and its date — that is what stops it being re-litigated every year.

## Replacing What Was Removed

| Removed | Nutrients that leave | Replacement, with the serving |
|---|---|---|
| Dairy | Calcium (~300 mg per 240 ml), iodine, B12, B2, protein | Calcium-set tofu 100 g (~350 mg), fortified plant milk **checked for both calcium and B12**, canned sardines with bones 100 g (~380 mg), iodized salt or a 150 µg supplement for the iodine |
| Eggs | Choline (~145 mg each), B12, selenium, protein | Soy, cruciferous vegetables, liver if eaten; choline often still short and worth naming |
| Wheat and gluten | Fiber, folate, iron, B vitamins (fortified in many countries) | Certified oats where tolerated, buckwheat, quinoa, legumes, teff |
| Fish | EPA/DHA, iodine, vitamin D, selenium | Algal oil 250-500 mg EPA+DHA, iodized salt, vitamin D supplement |
| Nuts | Magnesium, vitamin E, fiber, healthy fats | Seeds where not also allergenic — pumpkin, sunflower, chia |
| Soy | Protein, calcium (if calcium-set tofu was the source), some B vitamins | Legumes, other calcium-set products, fortified alternatives |
| Red meat | Heme iron, zinc, B12 | Poultry and fish keep heme iron; on a full exclusion, non-heme iron with vitamin C plus a zinc source, and B12 monitoring |
| Multiple groups at once | Compounding gaps that no single swap covers | Stop and count total coverage before agreeing to the next exclusion (`tracking.md`) |

## Hidden Sources

The places a "removed" food comes back:

- **Milk**: whey, casein, caseinate, ghee, lactose in medications and supplements, "non-dairy" creamers that legally contain caseinate.
- **Egg**: albumin, lysozyme (in some cheeses and wines), meringue, some pasta, glazes.
- **Wheat and gluten**: soy sauce, malt, seitan, some stock cubes, communion wafers, some medication binders, shared toasters and fryers for celiac.
- **Soy**: lecithin (usually tolerated even in soy allergy, but declared), hydrolyzed vegetable protein, many processed foods.
- **Fish and shellfish**: Worcestershire sauce (anchovy), Caesar dressing, some kimchi, fish sauce, surimi.
- **Nuts**: marzipan, pesto, mortadella, some sauces and desserts, cross-contamination in bulk bins.
- **Sesame**: tahini in hummus and halva, "spices" in some jurisdictions before declaration rules changed.
- **Supplements and medications** carry lactose, gelatin, soy, and wheat starch as excipients. Check them whenever a restriction and a supplement recommendation meet (`supplements.md`).

## Tests That Do Not Work

Saying so early saves money and prevents unnecessary restriction, which is itself a harm.

- **IgG food-sensitivity panels**: IgG indicates exposure, not intolerance. Major allergy organizations advise against them for diagnosing food reactions, and they routinely produce long "avoid" lists that shrink the diet with no basis.
- **Hair analysis, applied kinesiology, bioresonance, cytotoxic and electrodermal testing**: no validity for food reactions.
- **Consumer microbiome kits marketed for food sensitivity**: not validated for individual dietary recommendations.
- What does work: allergist testing for IgE allergy, hydrogen breath tests for lactose and fructose malabsorption, celiac serology and biopsy for celiac, and a structured elimination with reintroduction for everything else.

**Write in the same turn**: a confirmed allergy or intolerance into `## Allergies and Intolerances` of `~/Clawic/data/health/profile.md` with its type, severity, reaction, and how it was confirmed; each observation during a trial into `## Reactions`; the protocol and its outcome into `artifacts/<food>-elimination.md` with its `## Boxes` line; the reintroduction dates into `## Due`; a chosen avoidance (not a diagnosis) into `config.yaml` under restrictions (`memory-template.md`). A food restored after a negative reintroduction gets removed from the profile and noted — the record has to be able to shrink.
