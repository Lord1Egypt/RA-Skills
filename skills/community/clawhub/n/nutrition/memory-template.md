# Working File Templates — Nutrition

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced; `~/Clawic/data/health/` is shared with every other health skill. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/nutrition/config.yaml` | Key by key, read-modify-write |
| Nutrient status, gaps and fixes, how they eat, box index, due dates | `~/Clawic/data/nutrition/memory.md` | Rewritten in place; stays small |
| Allergies, intolerances, conditions, medications, life stage | `~/Clawic/data/health/profile.md` (**shared**) | One entry per fact, updated in place |
| Lab values (ferritin, 25-OH D, B12, folate, CRP, any marker) | `## Labs` in `~/Clawic/data/health/profile.md` (**shared**); `~/Clawic/data/health/<marker>.md` once one marker passes ~15 readings | One row per marker per date, append-only |
| Per-nutrient standing status: current estimate, source, target, last review | `## Nutrient Status` in `memory.md`; `~/Clawic/data/nutrition/nutrients.md` from ~15 nutrients | One row per nutrient |
| Supplements taken now, and the ones stopped and why | `## Supplements` in `memory.md`; `~/Clawic/data/nutrition/supplements.md` from ~15 rows | One row per product |
| The user's recurring foods with the nutrients they actually deliver | `## Usual Foods` in `memory.md`; `~/Clawic/data/nutrition/foods.md` from ~15 foods | One row per food |
| Food → symptom observations during intolerance or elimination work | `## Reactions` in `memory.md`; `~/Clawic/data/nutrition/reactions.md` from ~15 rows | One row per observation |
| Weekly or monthly coverage rollups | `~/Clawic/data/nutrition/intake/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read whole — repletion protocols, elimination-and-reintroduction plans and their outcome, a clinician's plan, an appointment summary, a food-swap plan | `~/Clawic/data/nutrition/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| The dietitian, physician, or allergist behind a plan | `~/Clawic/data/contacts/contacts.md` (**shared**) — name only, referenced from here | One row per person |
| Retests, stack reviews, reintroduction dates, seasonal checks | `## Due` in `memory.md` | The date is updated, the row is not duplicated |
| **Anything durable this table does not name** | `~/Clawic/data/nutrition/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A nutrient was found short, repleted, or re-estimated | Its row in `## Nutrient Status` |
| A lab value was read, reported, or retested | Its row in `## Labs` of `health/profile.md`, plus the retest date in `## Due` |
| An allergy, intolerance, condition, medication, or life stage came up | Its entry in `health/profile.md` |
| A supplement was started, changed in dose or form, or stopped | Its row in `## Supplements`, with the reason and the review date |
| A food entered the rotation, or its nutrient profile was worked out | Its row in `## Usual Foods` |
| A symptom followed a food, or an elimination or reintroduction day passed | Its row in `## Reactions` |
| A coverage rollup ran | A row in `intake/<year>.md` |
| A repletion protocol, elimination plan, clinician plan, or appointment summary was produced | `artifacts/` |
| A clinician was named as the source of a plan | `contacts/contacts.md`, referenced here by name only |
| A Red Flags signal fired and something was declined | One line in `## Notes` of `memory.md`, so the next session does not restart it |
| The user declared a preference | Its key in `config.yaml` |
| A recurring check was agreed or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, coverage rollups, and the shared health and contacts boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings, and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/nutrition/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Nutrient Status` → `nutrients.md`, `## Supplements` → `supplements.md`, `## Usual Foods` → `foods.md`, `## Reactions` → `reactions.md`, each keeping its own heading inside the new file.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a repletion protocol or an elimination plan is born as its own file whatever its size, because it is read whole and only when its subject comes up. Coverage rollups are the other exception: they are a dated log and never live in `memory.md`.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Lab reports, patient-portal exports, and health-app backups are the ones that carry them. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:labcorp-portal` · `env:HEALTH_API_TOKEN` · `1password:Personal/MyChart` · `bitwarden:Personal/Pharmacy` · `file:~/exports/labs-2026.pdf`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `portal password: <keychain:labcorp-portal>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: nutrient names and amounts, lab values with their dates and units, reference ranges, supplement brands, forms and doses, allergy and intolerance names, condition and medication names, the lab or clinic name, food and recipe names. **Secrets, strip them**: patient-portal and pharmacy logins, health-app API tokens and export keys, insurance member and policy numbers, national health or social security identifiers, full dates of birth paired with an identifier, and any account number appearing in a pasted report.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared health box](#shared-health-box) · [shared contacts box](#shared-contacts-box) · [intake/](#intake) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/nutrition/` if it does not exist.

```yaml
reference_standard: efsa-drv
lab_units: si
units: metric
diet_pattern: vegetarian
supplement_posture: food-first
tracking_depth: priority-nutrients
review_cadence: weekly
food_database: CIQUAL

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
restrictions:
  avoids: [pork, shellfish]          # chosen avoidance, not a diagnosed allergy
conventions:
  servings: hand-measures
  display: absolute                   # absolute amounts rather than %DV
platform:
  country: ES                         # no folic-acid flour fortification; iodized salt optional
output_register: food-first
```

A diagnosed allergy, intolerance, condition, or medication is **not** a preference: it goes in `~/Clawic/data/health/profile.md`. If you find one recorded in `config.yaml` or `memory.md`, move it there and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Nutrition Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Coverage rollups 2026 (31 weeks) → `intake/2026.md`; read before any "how am I doing" or trend question
- Iron repletion protocol → `artifacts/iron-repletion.md`; read at every ferritin retest until stores are back
- Dairy elimination and reintroduction → `artifacts/dairy-elimination.md`; read while the trial runs and before reintroducing anything else
- Usual foods (22) → `foods.md`; read before estimating coverage or proposing a swap
- Health profile (shared) → `~/Clawic/data/health/profile.md`; read before naming any food, dose, or supplement

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Ferritin retest | 12 weeks after any iron change | 2026-05-04 | 2026-07-27 |
| Supplement stack review | quarter | 2026-04-10 | 2026-07-10 |
| Coverage rollup | week | 2026-07-20 | 2026-07-27 |
| Vitamin D seasonal check | October and March | 2026-03-02 | 2026-10-01 |
| Dairy reintroduction day 1 | once | — | 2026-08-03 |

## Nutrient Status
| Nutrient | Estimated intake | Target | Status | Evidence | Reviewed |
|---|---|---|---|---|---|
| Iron | ~11 mg/day | 18 mg | short, repleting | ferritin 14 ng/mL 2026-05-04 | 2026-07-20 |
| Vitamin D | ~200 IU/day diet | 600 IU | covered by supplement | 25-OH D 31 ng/mL 2026-04-02 | 2026-07-20 |
| B12 | fortified sources only | 2.4 µg | watch | vegetarian since 2024 | 2026-07-20 |
| Fiber | ~19 g/day | 25 g | ramping, +5 g/week since 2026-07-06 | 3-day estimate | 2026-07-20 |

## Supplements
| Product | Nutrient and dose | Form | Timing | Why | Started | Review or stop |
|---|---|---|---|---|---|---|
| Iron 25 mg | elemental iron 25 mg | bisglycinate | alternate mornings, with orange juice, away from tea | ferritin 14 | 2026-05-06 | ferritin retest 2026-07-27 |
| D3 1000 IU | vitamin D 1000 IU | D3, with a fat-containing meal | daily, breakfast | winter 25-OH D 18 | 2026-11-02 | March check |
| Stopped: multivitamin | — | — | — | duplicated iron and zinc, pushed the stack near the zinc UL | — | stopped 2026-05-06 |

## Usual Foods
| Food | Typical serving | Notable nutrients per serving | Notes |
|---|---|---|---|
| Lentils, cooked | 200 g | ~6.6 mg iron (non-heme), ~8 g fiber | pair with peppers or citrus; not with tea |
| Greek yogurt | 170 g | ~200 mg calcium, ~17 g protein | main calcium source since dairy stayed in |

## Reactions
| Date | Food | Amount | Symptom | Onset | Notes |
|---|---|---|---|---|---|
| 2026-07-14 | milk, latte | 250 ml | bloating, cramping | ~90 min | second occurrence; hard cheese has been fine |

## Gaps and Fixes
Iron is the live one: repletion running since May. Fiber ramp started July 6 after the low-FODMAP trial ended.

## How They Work
Cooks at home five nights a week, no interest in weighing food, wants the swap rather than the explanation. Reads labs closely.

## Notes
2026-06-02: declined to recommend a 5000 IU vitamin D dose without a current 25-OH D — asked again on 2026-06-20, same answer.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every retest, review, seasonal check, and reintroduction date this skill sets belongs here, and the row's date is updated rather than a second row added.
- **`## Nutrient Status`**: `Status` is one of `covered`, `watch`, `short`, `repleting`, `over` — and `Evidence` says which it rests on, a lab or an intake estimate. A status with no evidence column is a guess with a table around it. Amounts always carry their unit; IU and µg are not interchangeable and the conversion differs per nutrient.
- **`## Supplements`**: a stopped product keeps its row with the reason, because the reason is what stops it being restarted next year. Doses are elemental where that differs from the compound (25 mg elemental iron, not 200 mg ferrous sulfate).
- **`## Reactions`**: only what was observed — food, amount, symptom, onset. No interpretation in the table; interpretation goes in the elimination artifact.
- These headings are exactly the ones the split-out files get, so the split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still mapping their diet, labs, and restrictions |
| `complete` | Diet, restrictions, labs, and supplement stack are known and current |

## Shared health box

Lives at `~/Clawic/data/health/profile.md` and is shared with every other health skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Health Profile

## Conditions
| Condition | Since | Notes | Source |
|---|---|---|---|
| Celiac disease | 2019 | biopsy-confirmed | clinician |

## Allergies and Intolerances
| Item | Type | Severity | Reaction | Confirmed by |
|---|---|---|---|---|
| Peanut | allergy | anaphylaxis | airway | allergist, 2015 |
| Lactose | intolerance | moderate | bloating within 90 min | elimination trial, 2026-07 |

## Medications and Supplements
| Name | Dose | Since | Notes |
|---|---|---|---|
| Levothyroxine | 75 µg | 2021 | fasting, 4 h from calcium and iron |
| Metformin | 1000 mg | 2023 | lowers B12 over years — annual B12 |

## Life Stage
Pregnancy, second trimester since 2026-06. Or: postmenopausal since 2024. Or: none recorded.

## Labs
| Date | Marker | Value | Unit | Reference range | Notes |
|---|---|---|---|---|---|
| 2026-05-04 | Ferritin | 14 | ng/mL | 15-150 | CRP 1.2, so not inflated |
| 2026-05-04 | Hemoglobin | 12.1 | g/dL | 12.0-15.5 | — |
| 2026-04-02 | 25-OH vitamin D | 31 | ng/mL | 30-100 | on 1000 IU/day |
```

- **Identity is the entry's name for a profile fact, and marker + date for a lab row.** Read the file before adding. If the condition, allergen, or medication is already there, update that entry in place — never append a second entry for the same thing, and never a second lab row for the same marker on the same date.
- **Never edit an entry another source wrote.** The `Source` or `Confirmed by` column says who owns it. A clinician-sourced entry is corrected only by the user telling you it changed, and then the source column changes with it.
- **Removal is part of the record.** A resolved condition, a stopped medication, or an allergy the user outgrew gets its row deleted and the date noted in `## Notes` of the nutrition `memory.md`. A profile that only grows becomes a list of things that used to be true.
- **Units live in the value's own column** (`14 ng/mL`, `75 µg`), and the reference range travels with the row: ranges are lab-specific, and a value without its range cannot be read next year. Never convert someone's stored value in place — add the converted figure in `Notes` and leave the original.
- **Scale cut**: labs stay in `## Labs` while any one marker has ≤15 readings. Past that, that marker moves to `~/Clawic/data/health/<marker>.md` with the same columns, and `## Labs` keeps one index line for it (`Ferritin (22 readings) → ferritin.md`). Only the marker that crossed moves; the rest stay.
- **Foreign columns win.** If `profile.md` already exists with a different structure or column set, match what is there and add anything missing as a trailing note. Never rewrite its headings.
- No credential, portal login, member number, or national identifier — ever (see Secrets).

## Shared contacts box

Only when a clinician is the source of a plan. Lives at `~/Clawic/data/contacts/contacts.md`, shared with every skill that names people.

```markdown
| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Dr. Elena Marsh | elena.marsh@clinic.example | dietitian | email | set the iron repletion plan | 2026-05-04 | — |
```

- **Identity is `Key`**: lowercase email, else a handle, else `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- Read before adding; if the key is there, update the row in place. Never touch a row another skill wrote beyond the fields you own.
- Past ~15 people, or as soon as one does not fit its row, each person moves to `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- The person is written there once; here and in artifacts they appear by name only. Duplicating the record is how two skills end up disagreeing about the same clinician.

## intake/

```markdown
# Coverage — 2026

| Week | Days logged | Fiber avg | Short | Over | Note |
|---|---|---|---|---|---|
| 2026-W29 | 5 | 19 g | iron, B12 | — | ramp week 2 |
| 2026-W30 | 6 | 22 g | B12 | — | lentils 3× |
```

- One row per `review_cadence` period, appended, never rewritten. `Short` and `Over` name nutrients, not scores — a score invites optimization and says nothing actionable.
- `Days logged` is the honesty column: a week built on two days of data is a hint, not a measurement, and the comparison with a six-day week is invalid.
- Cut by year. A year file is closed by leaving it alone; never merge years.

## artifacts/

One file per thing, at `~/Clawic/data/nutrition/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **repletion protocol**, **elimination and reintroduction plan with its outcome**, **a clinician's plan as given**, **appointment summary**, **food-swap plan**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Iron repletion — started 2026-05-06
*Read at every ferritin retest until stores are back. Written 2026-05-06.*

Trigger: ferritin 14 ng/mL, CRP 1.2 (not inflated), premenopausal, vegetarian.
Protocol: 25 mg elemental iron as bisglycinate, alternate mornings, with 150 ml orange juice, ≥2 h from tea, coffee, calcium, and the levothyroxine dose.
Retest: ferritin + hemoglobin at 12 weeks (2026-07-27); continue 3-6 months past hemoglobin normalizing to refill stores.
Stop rule: ferritin above 50 ng/mL, or a clinician says so.
Outcome: <filled at each retest, with the date>
```

```markdown
# Dairy elimination and reintroduction
*Read while the trial runs and before reintroducing anything else. Written 2026-07-14.*

Removed: all dairy, 2026-07-16 to 2026-08-02 (17 days).
Replaced: calcium from set tofu and fortified soy — the exclusion removed ~600 mg/day, and the replacement is the half people skip.
Symptoms tracked: bloating, cramping, stool form — daily rows in `## Reactions`.
Reintroduction: hard cheese day 1, yogurt day 4, milk day 7, one food at a time, 72 h apart.
Outcome: <what happened, and what went into health/profile.md as a result>
```

A clinician's plan is transcribed as given, with the clinician's name pointing at `contacts/contacts.md`, and is never silently edited to match this skill's defaults — where they disagree, the clinician's numbers win and the disagreement is noted below the plan.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact heading it had inside `memory.md`.

`nutrients.md` — `## Nutrient Status`. Exists once the user tracks more nutrients than the Priority table.

`supplements.md` — `## Supplements`, plus a `## Stopped` heading once the stopped rows outnumber the active ones. The stopped list is the reason this file earns its existence: it is the record of what was tried and why it ended.

`foods.md` — `## Usual Foods`. The nutrient profile of a food is worked out once and reused; without this file it is re-derived every few weeks with slightly different numbers.

`reactions.md` — `## Reactions`. Exists during and after elimination work, and stays: a reaction history two years old is what stops a resolved intolerance being re-litigated.
