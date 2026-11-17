# Labs — Reading Nutrient Blood Work

A nutrient marker is worth ordering only if it changes what happens next. Most do not: there is no useful routine test for magnesium, potassium in a healthy person, or most B vitamins. The five that earn their place are ferritin, 25-OH vitamin D, B12, folate, and — as the interpreter of the first — CRP.

**Before reading any result**, read `## Labs` in `~/Clawic/data/health/profile.md` (or `health/<marker>.md` if `## Boxes` points there) and the medications listed there. A single value is a snapshot; the same marker six months ago is what makes it a direction. `lab_units` decides whether figures print conventional or SI.

**Contents:** [Units and Conversions](#units-and-conversions) · [The Markers Worth Ordering](#the-markers-worth-ordering) · [Markers That Mislead](#markers-that-mislead) · [Confounders That Invalidate a Result](#confounders-that-invalidate-a-result) · [Retest Intervals](#retest-intervals) · [Reading a Panel Together](#reading-a-panel-together) · [Interpreting Without a Lab](#interpreting-without-a-lab)

## Units and Conversions

The same value looks like deficiency or sufficiency depending on the unit, and labs in different countries print different ones. Convert before comparing anything.

| Marker | Conventional | SI | Conversion |
|---|---|---|---|
| 25-OH vitamin D | ng/mL | nmol/L | ng/mL × 2.496 = nmol/L. 20 ng/mL = 50 nmol/L; 30 ng/mL = 75 nmol/L |
| Vitamin B12 | pg/mL | pmol/L | pg/mL × 0.738 = pmol/L. 200 pg/mL ≈ 148 pmol/L |
| Ferritin | ng/mL | µg/L | 1:1 — the numbers are identical, only the label changes |
| Folate, serum | ng/mL | nmol/L | ng/mL × 2.266 = nmol/L |
| Hemoglobin | g/dL | g/L | g/dL × 10 = g/L |
| Homocysteine | µmol/L | µmol/L | Same unit everywhere |

Never rewrite a stored value into another unit. Add the conversion in the notes column and leave the original as the lab reported it (`memory-template.md`).

## The Markers Worth Ordering

| Marker | What it measures | Thresholds worth knowing | Reading it |
|---|---|---|---|
| **Ferritin** | Iron stores | <15 ng/mL depleted (WHO adult threshold); <30 often symptomatic; >200-300 warrants a cause | The single best iron-status test — and an acute-phase reactant, so it must be read with CRP |
| **CRP** | Inflammation | <1 mg/L low, >3 mg/L raises the question, >10 mg/L means acute | Not a nutrient marker. It is the interpreter that says whether ferritin and zinc can be believed |
| **Hemoglobin / MCV** | Anemia and its shape | Anemia below ~13 g/dL M, ~12 g/dL F | Low MCV points to iron; high MCV points to B12 or folate; the two together can cancel to a normal MCV, which is why ferritin and B12 both get ordered |
| **25-OH vitamin D** | Vitamin D status | <20 ng/mL (50 nmol/L) deficient per IOM; 20-30 insufficient per the Endocrine Society; >100 ng/mL toxicity concern | Order 25-OH D, never 1,25-dihydroxy — the active form stays normal or even rises during deficiency and is the classic wrong test |
| **B12** | Serum B12 | <200 pg/mL deficient; 200-300 borderline and needs MMA; >300 usually adequate | Serum B12 is insensitive: symptoms occur inside the "normal" range, and metformin, PPIs, and pregnancy all shift it |
| **MMA (methylmalonic acid)** | Functional B12 at the cell | Elevated MMA with a borderline B12 confirms deficiency | The tiebreaker for the 200-300 band. Kidney impairment raises it independently |
| **Homocysteine** | Functional B12, folate, B6 | Elevated with any of the three low | Non-specific — it tells you something in that group is short, not which |
| **RBC folate** | Folate status over ~3 months | Below the lab's range | Better than serum folate, which reflects the last few meals |
| **Serum zinc** | Zinc, poorly | Below the lab's range, read with CRP | Falls with inflammation, falls after a meal, and falls with low albumin. Fasting sample or do not bother |

## Markers That Mislead

| Test | Why it misleads | What to do instead |
|---|---|---|
| Serum magnesium | Roughly 1% of body magnesium is extracellular; the body defends serum levels while tissue depletes | Estimate intake, treat with food, and accept that no routine test settles it |
| 1,25-dihydroxy vitamin D | Rises in deficiency through PTH stimulation, so it reads reassuring at the worst moment | 25-OH D, always |
| Serum iron alone, or "iron saturation" without ferritin | Swings with the last meal and time of day | Ferritin with CRP; transferrin saturation only as an adjunct |
| Serum folate | Reflects recent intake, so a single good week normalizes it | RBC folate for status |
| Serum calcium | Tightly regulated by PTH; it is normal until something is seriously wrong | It is a calcium-*regulation* test, not a calcium-*intake* test — intake math is the tool for intake |
| Hair mineral analysis | Not standardized, contaminated by shampoo and water, and unvalidated for nutrient status | Nothing — decline to interpret it and say why |
| Direct-to-consumer "full vitamin panels" | Wide panels generate incidental abnormalities that trigger supplements nobody needed | Order or read only markers with a decision attached |
| IgG food-sensitivity panels | IgG to a food indicates exposure, not intolerance; major allergy bodies advise against them | Structured elimination and reintroduction (`restrictions.md`) |

## Confounders That Invalidate a Result

Check these before interpreting; each one turns a number into noise.

- **Inflammation or recent infection** — inflates ferritin, deflates zinc, iron, and selenium. Repeat when CRP is back down.
- **Recent supplementation** — a B12 result taken after starting a B12 supplement measures the supplement. Stop for the interval the ordering clinician specifies, or read the value as "on treatment".
- **High-dose biotin** — distorts many immunoassays, including thyroid, troponin, and some vitamin assays, in either direction. Stop 48-72 hours before the draw and tell the lab.
- **Pregnancy** — dilutional changes lower ferritin, hemoglobin, and B12 legitimately; pregnancy-specific ranges apply (`populations.md`).
- **Time of day and fasting state** — serum iron and zinc move with both.
- **Hemolyzed sample** — falsely raises potassium and some minerals; the lab usually flags it, and a flagged sample is repeated, not interpreted.
- **Kidney impairment** — raises MMA and homocysteine independently of B12.

## Retest Intervals

| Situation | Retest at | Why that interval |
|---|---|---|
| Started or changed oral iron | 8-12 weeks | Hemoglobin responds in weeks; ferritin lags. Earlier than 8 weeks reads as failure when it is timing |
| Iron repletion continuing | Every 3 months until ferritin is comfortably in range, then stop | Stores need 3-6 months beyond hemoglobin normalizing |
| Started vitamin D | ~3 months | Steady state on a fixed dose takes roughly that long |
| Vitamin D stable and supplemented | Annually, or October and March if seasonal swing matters | Two points a year capture the swing that one does not |
| Started oral B12 | ~3 months | Serum B12 rises quickly; MMA is the marker that shows the tissue effect |
| Vegan, no symptoms | B12 annually; ferritin and 25-OH D at whatever interval the clinician sets | The predictable gaps get a schedule rather than a scare |
| Post-bariatric | On the surgical team's schedule, lifelong | Deficiencies arrive on a timetable here (`conditions.md`) |
| After any deficiency resolves | One confirmation at 6-12 months | Resolution without a confirming retest is an assumption |

Every interval above becomes a dated row in `## Due`, not a sentence in a reply.

## Reading a Panel Together

Patterns beat single values:

- **Low ferritin + low MCV + low hemoglobin** — iron deficiency anemia. Treat, and find the blood loss.
- **Low ferritin + normal hemoglobin** — depleted stores without anemia. Symptomatic often enough to treat, and the earliest point at which treating is easy.
- **Normal-to-high ferritin + high CRP** — uninterpretable for iron. Repeat when the inflammation clears.
- **High MCV + low B12 or low folate** — megaloblastic picture. Establish B12 status before giving folate, always (`safety.md`).
- **Low B12 + high MMA + high homocysteine** — functional B12 deficiency, treat regardless of where serum B12 sits in the range.
- **Normal B12 + high MMA** — early or functional deficiency, common in older adults with atrophic gastritis.
- **High ferritin, no inflammation, transferrin saturation >45%** — iron overload question, not a nutrition question. Clinician (`safety.md`).
- **Everything normal, symptoms persist** — a complete answer. Say it plainly and stop adding markers.

## Interpreting Without a Lab

Most sessions have no blood work, and the honest answer is a status of `watch` rather than a diagnosis:

- Name what the intake estimate supports and what it cannot: "your intake is below the RDA; whether your stores are low is a ferritin question."
- Give the food fix regardless — food never needs a test.
- Give the supplement only when the pattern makes the gap near-certain and the nutrient is safe without measurement: B12 on a vegan diet and vitamin D in winter qualify; iron does not (SKILL.md Rule 4).
- Name the test worth asking a clinician for, so the next appointment produces the answer instead of another guess.

**Write in the same turn**: every value into `## Labs` of `~/Clawic/data/health/profile.md` with its date, unit, and the lab's own reference range; the interpretation into the nutrient's `## Nutrient Status` row; the retest into `## Due` (`memory-template.md`). Once a single marker passes ~15 readings it moves to `~/Clawic/data/health/<marker>.md` with the same columns, and `## Labs` keeps one index line for it. The reference range is stored with the value because ranges are lab-specific and a bare number is unreadable two years later.
