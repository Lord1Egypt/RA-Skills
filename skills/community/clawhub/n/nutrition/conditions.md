# Conditions — Diagnoses That Rewrite the Nutrition Answer

A diagnosis changes which nutrients are at risk, which advice inverts, and who owns the numbers. In every case here the clinician's targets win; this skill's job is to know what to monitor, what to replace, and where the general advice stops applying.

**Before answering anything in this file**, read the conditions and medications in `~/Clawic/data/health/profile.md` and the current stack in `## Supplements`. A condition present and unread turns standard advice into bad advice — potassium encouragement in CKD is the cleanest example.

**Contents:** [Malabsorptive Conditions](#malabsorptive-conditions) · [Celiac Disease](#celiac-disease) · [IBD](#ibd) · [Bariatric Surgery](#bariatric-surgery) · [Kidney Disease](#kidney-disease) · [Type 2 Diabetes and Insulin Resistance](#type-2-diabetes-and-insulin-resistance) · [GLP-1 Receptor Agonists](#glp-1-receptor-agonists) · [Thyroid](#thyroid) · [Anemias](#anemias) · [Liver Disease and Alcohol Use](#liver-disease-and-alcohol-use) · [Osteoporosis](#osteoporosis) · [Cardiovascular and Hypertension](#cardiovascular-and-hypertension)

## Malabsorptive Conditions

The shared pattern, worth holding as one idea: anything that damages the small intestine, removes it, or starves it of bile and pancreatic enzymes puts the **fat-soluble vitamins (A, D, E, K), iron, B12, zinc, magnesium, and calcium** at risk simultaneously. Signs that point at malabsorption rather than intake: pale, floating, foul-smelling stools; weight loss despite adequate eating; multiple deficiencies at once. Multiple simultaneous deficiencies is itself the diagnostic clue — a single low nutrient is a diet question, four low nutrients is an absorption question.

## Celiac Disease

- **Screen before removing gluten.** Serology and biopsy require gluten in the diet; removing it first means a supervised gluten challenge later to get an answer.
- At diagnosis, the standard nutrient screen covers iron, ferritin, folate, B12, vitamin D, calcium, and zinc — the villous damage impairs all of them, and several are typically low at presentation.
- Bone density is affected by long-standing untreated celiac; calcium and vitamin D adequacy is part of the treatment, not an extra.
- The gluten-free diet itself then creates a second gap list — fiber, folate, iron, B vitamins — because most gluten-free flours are unfortified (`patterns.md`).
- **Cross-contamination matters here in a way it does not for a preference**: shared toasters, fryers, flour dust, and bulk bins. Oats must be certified gluten-free, and a minority of people with celiac react to oats regardless.
- Persistent symptoms on a strict gluten-free diet is a clinician question — refractory celiac, another diagnosis, or hidden gluten.
- Dermatitis herpetiformis is celiac presenting on the skin, and it carries the same dietary requirement.

## IBD

Crohn's disease and ulcerative colitis, and the distinction matters nutritionally.

- **Crohn's** can affect any part of the tract; terminal ileal disease or resection specifically impairs **B12 and bile acid** handling, which cascades into fat-soluble vitamin malabsorption.
- **Ulcerative colitis** is colonic: blood loss drives iron deficiency, and iron is the dominant nutritional issue.
- Active flares are a low-residue, clinician-directed situation; the fiber advice in `gut.md` and `diet-quality.md` applies in remission, not during a flare.
- Corticosteroid courses add calcium, vitamin D, and potassium concerns (`interactions.md`).
- Oral iron can worsen GI symptoms in active disease, which is one reason intravenous iron is used — a clinician's decision, and a reason not to push oral iron here.
- Nutrition status is part of disease management, not a side conversation: monitoring is scheduled by the gastroenterology team and this skill supports it.

## Bariatric Surgery

Lifelong, structural, and predictable — the deficiencies arrive on a timetable rather than by chance. Restrictive procedures (sleeve) and malabsorptive ones (bypass, duodenal switch) differ in severity, and the surgical team's protocol governs.

| Nutrient | Why | Standard handling |
|---|---|---|
| B12 | Reduced acid and intrinsic factor | Lifelong supplementation, monitored |
| Iron | Reduced acid and bypassed duodenum | Supplementation, often at higher doses, with monitoring |
| Calcium | Bypassed duodenum, low acid | **Citrate, not carbonate** — carbonate needs acid that is no longer there. Split doses at 500 mg |
| Vitamin D and the other fat-soluble vitamins | Fat malabsorption, more so after malabsorptive procedures | Supplemented and monitored, often at doses above the ordinary UL under clinical direction |
| Thiamin | Reduced intake, vomiting, rapid weight loss | An acute risk with persistent vomiting — a clinical emergency, not a supplement adjustment |
| Protein | Restricted volume | Targets set by the team; this skill supports adherence, not the number |
| Zinc, copper, selenium | Malabsorption | Monitored on the team's schedule; zinc supplementation without copper monitoring is the common error |

Blood work runs on the surgical team's lifelong schedule. Anyone post-bariatric who has stopped attending follow-up is at real risk, and saying so is appropriate.

## Kidney Disease

**The file where general advice inverts.** Everything the rest of this skill encourages — potassium, phosphorus, protein volume, and salt substitutes — may be restricted here, and the restriction is staged by kidney function.

- **Potassium**: encouraged everywhere else, restricted here depending on stage and serum potassium. **Potassium-chloride salt substitutes are hazardous**, especially alongside ACE inhibitors, ARBs, or potassium-sparing diuretics.
- **Phosphorus**: the distinction that matters is source. Phosphate **additives** are absorbed nearly completely, against roughly 40-60% for organic phosphorus in whole foods. Cutting additive-laden processed food achieves more than cutting dairy and legumes, and costs less nutritionally. Additives appear on ingredient lists as "phos-" compounds.
- **Protein**: restriction is staged and clinician-set; over-restriction causes malnutrition, so this is not a place for a default.
- **Sodium and fluid**: usually restricted, with the amounts set by the team.
- **Vitamin D**: activation is impaired; specific forms are prescribed.
- **Never give a CKD user the standard DASH-style advice.** Check the profile first; that check is the whole point of Rule 1.

## Type 2 Diabetes and Insulin Resistance

- Fiber, particularly viscous soluble fiber, slows glucose absorption; whole-grain and legume-forward patterns are the food-level intervention (`diet-quality.md`).
- Metformin depletes B12 over years — annual B12 monitoring is the standard follow-through, and it is routinely forgotten (`interactions.md`).
- Magnesium status is often lower in type 2 diabetes; food sources are the answer given the poor supplemental evidence for glycemic outcomes.
- Chromium, cinnamon, berberine, and similar supplements are widely sold for glycemic control; trial results are small and inconsistent, and none replaces medication. Say that plainly.
- Any change likely to lower glucose in someone on insulin or a sulfonylurea is a hypoglycemia risk and belongs with the prescriber before the diet changes.
- Glycemic index is a useful concept and a poor tool alone: the mixed meal, the fat and protein alongside, ripeness, and processing all move it more than the published number.

## GLP-1 Receptor Agonists

A growing and distinctive case: intake falls sharply, so nutrient density per calorie becomes the whole design problem.

- Total intake can drop far enough that micronutrient coverage fails even on a "good" diet — this is the situation `tracking_depth: full-panel` exists for.
- Protein and calcium matter for preserving lean mass and bone during rapid loss; the protein target is `calories`' number.
- Common side effects — nausea, early satiety, constipation, reflux — shape what is realistically eaten. Fiber and fluid handling matters, and constipation is frequent (`gut.md`).
- Dose targets, weight targets, and anything about the medication itself belong to the prescriber.
- A multivitamin is more defensible here than in almost any other situation in this skill, because the shortfall is caused by volume rather than by choice.

## Thyroid

- **Iodine is both a requirement and a risk**: deficiency causes hypothyroidism and goiter, and excess can trigger thyroid dysfunction in susceptible people. Kelp supplements are the usual route to excess and are best avoided in favor of measured iodine.
- **Levothyroxine timing** is non-negotiable: fasting, and at least 4 hours from calcium, iron, and magnesium (`interactions.md`). This single instruction resolves a large share of "my dose stopped working".
- Selenium has a role in thyroid metabolism and some trial interest in autoimmune thyroiditis; the UL is 400 µg and Brazil nuts make it easy to approach.
- Goitrogens in cruciferous vegetables and soy are a practical non-issue at ordinary intakes with adequate iodine — soy can affect levothyroxine absorption, which is a timing question rather than an avoidance one.

## Anemias

- **Iron deficiency anemia**: treat, and find the cause. Heavy menstrual bleeding is the most common in premenopausal women; GI bleeding is the one that must be excluded in men and postmenopausal women, and it is a Red Flag (`safety.md`).
- **B12 or folate deficiency (macrocytic)**: establish B12 status before giving folate, always.
- **Pernicious anemia**: autoimmune loss of intrinsic factor. Clinician-managed, and lifelong.
- **Anemia of chronic disease**: iron is present but sequestered; ferritin is normal or high while iron is functionally unavailable. Supplementing iron here does not help and is not harmless.
- **Thalassemia trait and other hemoglobinopathies**: microcytosis without iron deficiency. Iron given on the basis of a low MCV alone is a real harm route — ferritin first, always.

## Liver Disease and Alcohol Use

- Alcohol use disorder depletes thiamin, folate, B6, magnesium, and zinc, and impairs absorption on top of it.
- **Thiamin before glucose** in a malnourished person is a clinical rule with serious consequences (Wernicke encephalopathy); this is a clinician's domain and appears here so it is recognized, not managed.
- Refeeding syndrome after prolonged inadequate intake involves phosphate, potassium, magnesium, and thiamin shifts and is a medical emergency — relevant after extended fasting or starvation (`fasting`, `safety.md`).
- Advanced liver disease inverts protein and sodium advice and is entirely clinician-directed.

## Osteoporosis

- Calcium 1200 mg and adequate vitamin D as the floor, with food-first sourcing; the calcium supplement and cardiovascular risk debate is unsettled, which is an argument for food.
- Vitamin K, magnesium, and protein all contribute to bone; protein adequacy is more often the missing piece than any of the micronutrients.
- Weight-bearing and resistance exercise is at least as important as any nutrient here (`fitness`).
- Bisphosphonate timing: taken fasting with plain water, well separated from calcium and food, per the prescribing instructions.

## Cardiovascular and Hypertension

- The DASH pattern and the sodium-to-potassium ratio are the evidence-backed levers (`diet-quality.md`).
- **Warfarin makes vitamin K a consistency question, not an avoidance question** — the swings destabilize INR, not the greens themselves (`interactions.md`).
- Saturated fat replaced by polyunsaturated fat lowers risk; replaced by refined carbohydrate, it does not. Name the replacement.
- Omega-3 supplementation for prevention is unsettled by dose and formulation; two portions of oily fish weekly is the defensible default.
- Potassium restriction inverts this whole section when CKD or a potassium-sparing medication is present. Check the profile.

**Write in the same turn**: the condition and its date into `## Conditions` of `~/Clawic/data/health/profile.md` with the source; its nutrient consequences into `## Nutrient Status` with the condition named as the evidence; the monitoring schedule the condition implies into `## Due`; and any clinician-set targets into `artifacts/<condition>-plan.md` transcribed as given, with the clinician referenced by name from `~/Clawic/data/contacts/contacts.md` (`memory-template.md`). Where the clinician's numbers and this skill's defaults disagree, the clinician's win and the disagreement is noted below the plan rather than quietly resolved.
