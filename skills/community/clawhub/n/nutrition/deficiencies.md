# Deficiencies — Symptom to Cause to Confirmation

Nutrient deficiency symptoms are non-specific by nature: the body runs out of a cofactor and the first thing that shows is tiredness. The chain that works is **symptom → shortlist → the one test that discriminates → treat → retest**. Skipping to treatment is how people end up on four supplements with the original symptom intact.

**Before working a symptom**, read `## Nutrient Status` and `## Supplements` in `~/Clawic/data/nutrition/memory.md`, and the conditions and medications in `~/Clawic/data/health/profile.md`. Half of the "deficiency symptoms" that arrive have a medication behind them (`interactions.md`), and a nutrient already being supplemented changes the shortlist entirely.

**Contents:** [The Order of Suspicion](#the-order-of-suspicion) · [Symptom Chains](#symptom-chains) · [Deficiency Timelines](#deficiency-timelines) · [Risk Multipliers](#risk-multipliers) · [When It Is Not Nutrition](#when-it-is-not-nutrition) · [Correcting a Confirmed Deficiency](#correcting-a-confirmed-deficiency)

## The Order of Suspicion

Work down this list before naming an exotic nutrient. Prevalence decides the order, not interest.

1. **Iron** — the most common nutrient deficiency worldwide, and concentrated in menstruating women, where roughly one in five to one in ten runs depleted stores depending on the population studied.
2. **Vitamin D** — near-universal in winter above ~40° latitude; the question is degree, not presence.
3. **B12** — vegans, adults 65+, and long-term metformin or PPI users; the one where delay causes permanent harm.
4. **Folate** — restricted diets, alcohol use, pregnancy, and countries without flour fortification.
5. **Magnesium and potassium** — intake shortfalls rather than diagnosable deficiencies for most people; the fix is food, and no useful test exists for magnesium.
6. **Zinc, iodine, selenium** — pattern-driven: the restricted diet or the geography names them before the symptom does.
7. **Everything else** — real but rare outside malabsorption, alcohol use disorder, bariatric surgery, or extreme diets.

## Symptom Chains

Read as: what the user says → what to suspect, in order → the discriminating test → the confound that fakes it.

| The user says | Suspect, in order | Discriminating test | The confound |
|---|---|---|---|
| "Tired all the time" | Iron, B12, D, thyroid, sleep, depression | Ferritin + CRP, B12, 25-OH D, TSH | Fatigue is the least specific symptom in medicine; a normal panel is a real answer and points elsewhere |
| Tired, pale, breathless on stairs, cold extremities | Iron deficiency ± anemia | Ferritin with CRP, then hemoglobin | Ferritin rises with any inflammation — a "normal" 45 with CRP 12 can still be depletion (`labs.md`) |
| Tingling, numbness, pins and needles, balance off | B12, then B6 excess, then thyroid, then diabetes | B12, MMA if 200-300 pg/mL; review every B6 source | Neurological B12 signs are the urgent branch — clinician this week, and never folate first |
| Hair shedding, diffuse, whole scalp | Iron, thyroid, rapid weight loss, protein shortfall, postpartum, illness 3 months back | Ferritin, TSH, and a timeline | Telogen effluvium lags its trigger by 2-3 months, so the cause is in the past, not in this week's diet. Ferritin thresholds cited for hair are higher than the anemia threshold and are contested |
| Cramps, twitching eyelid, poor sleep | Magnesium intake, potassium, dehydration, exertion, statins | Intake math; potassium only if a condition demands | Serum magnesium reflects roughly 1% of body stores and reassures falsely (`labs.md`) |
| Cracks at the mouth corners, sore red tongue | Riboflavin, B6, iron, B12 | Ferritin, B12, and a look at the whole diet pattern | Angular cheilitis is also fungal and also mechanical — a nutrient answer is not the only one |
| Frequent colds, slow healing, food tastes flat | Zinc | Serum zinc with CRP; diet estimate first | Serum zinc falls with inflammation and after a meal — fasting sample, read with CRP |
| Bone pain, muscle weakness, falls | Vitamin D ± calcium | 25-OH D | Falls in an older adult are a clinician question regardless of the vitamin D number |
| Poor night vision, dry eyes | Vitamin A, usually with fat malabsorption | Ask about steatorrhea, surgery, celiac, alcohol before ordering anything | In fortified countries this is almost always malabsorption, not intake |
| Bruises easily, gums bleed | Vitamin C, vitamin K, medications, platelet issues | Produce intake over the last month; medication review | Genuine scurvy still happens — in isolated older adults, severe restriction, and alcohol use disorder |
| Restless legs, worse at night | Iron | Ferritin | The threshold used here is ~75 ng/mL (IRLSSG), far above the anemia threshold; a "normal" ferritin of 40 is still low for this indication, and oral iron is trialled below it |
| Brittle, spooned, or ridged nails | Iron (koilonychia), rarely biotin | Ferritin | Longitudinal ridges are an aging finding, not a deficiency |
| Mouth ulcers, recurring | Iron, B12, folate, celiac | Ferritin, B12, folate, and a celiac screen if the pattern fits | Recurrent aphthous ulcers are often idiopathic |
| Skin: dermatitis, cracked, photosensitive | Niacin, zinc, essential fatty acids | Dietary pattern; clinician for anything progressive | Rare outside alcohol use disorder or severe malabsorption |
| "I feel awful and everything is normal" | Nothing in this file | Stop; sleep, mood, thyroid, medication, and workload first | Adding supplements to a normal panel is how a stack starts |

## Deficiency Timelines

How long a stopped intake takes to show, which is what decides whether the diet three months ago is a suspect.

| Nutrient | Body stores last | Practical consequence |
|---|---|---|
| B12 | 2-5 years in a healthy liver | A vegan diet started last year has not caused it yet; a diet started in 2021 has |
| Vitamin A | Months | Malabsorption, not last month's carrots |
| Iron | Weeks to months, and ferritin falls before hemoglobin does | Ferritin is the early-warning marker; anemia is the late one |
| Folate | Weeks to ~4 months | Pregnancy timing matters: the neural tube closes by week 4, before most people know |
| Vitamin D | Weeks to months (adipose-bound) | Summer stores drain by midwinter; the seasonal check is October and March |
| Vitamin C | ~1 month to symptomatic depletion | Scurvy needs a genuinely produce-free month, not a bad week |
| Thiamin | ~2-3 weeks | The reason refeeding after starvation or a long fast is a clinical event (`safety.md`) |
| Water-soluble B vitamins generally | Days to weeks | A short bad stretch does not deplete them; a pattern does |

## Risk Multipliers

A person with two of these does not get the general answer. Check them before running any chain above.

- **Malabsorption**: celiac, IBD, pancreatic insufficiency, bariatric surgery, chronic diarrhea — puts every fat-soluble vitamin, iron, B12, and zinc at risk at once (`conditions.md`).
- **Medications**: metformin and PPIs on B12; PPIs on magnesium, iron, and calcium; diuretics on potassium, magnesium, and zinc; some anticonvulsants on folate and vitamin D (`interactions.md`).
- **Alcohol use**: thiamin, folate, B6, magnesium, zinc — the whole B group, plus impaired absorption and increased losses.
- **Diet pattern**: each one has its own gap list, and they are predictable enough to run without a symptom (`patterns.md`).
- **Life stage**: pregnancy, breastfeeding, adolescence, and 65+ move both the requirement and the absorption (`populations.md`).
- **Blood loss**: heavy periods, frequent donation, GI bleeding — the first is the single most common cause of iron deficiency in women, and the last is a Red Flag.
- **Bariatric surgery**: lifelong, structural, and the deficiencies arrive on a schedule rather than by chance.

## When It Is Not Nutrition

Say this out loud rather than searching for a nutrient that fits:

- Fatigue with normal iron, B12, D, and thyroid is a sleep, mood, activity, or workload question, and supplements will not touch it.
- Any symptom that is progressive, one-sided, or accompanied by fever, weight loss, or bleeding leaves this skill entirely (`safety.md`).
- Symptoms that started with a new medication are a medication question until proven otherwise.
- Hair, nails, and skin respond slowly to everything; three weeks of a supplement proves nothing in either direction.

## Correcting a Confirmed Deficiency

Once a test confirms it, the fix has four parts, and skipping the fourth is why deficiencies recur:

1. **Repletion dose** — higher than the RDA and time-limited, sized to the nutrient and the depth of the deficit (`supplements.md`).
2. **The cause** — heavy periods, a medication, a malabsorptive condition, a diet gap. A repletion that does not name the cause has scheduled its own repeat.
3. **Maintenance** — what intake holds the level once repletion ends: food, a lower dose, or nothing.
4. **Retest date** — SKILL.md Rule 7 intervals, written into `## Due`.

**Write in the same turn**: the nutrient's row in `## Nutrient Status` with the evidence, the lab value in `## Labs` of `~/Clawic/data/health/profile.md`, the retest in `## Due`, and — for anything with a multi-month protocol like iron repletion — the protocol itself as `artifacts/<nutrient>-repletion.md` with its `## Boxes` line (`memory-template.md`). The protocol is the file that gets re-read at every retest; without it, month three re-invents the dose.
