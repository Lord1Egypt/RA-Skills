---
name: interpretive-lab-comment-drafter
description: >
  Use this skill when a clinical laboratory scientist (MLS/MT/CLS), pathologist,
  or lab director needs to draft an interpretive comment for a complex laboratory
  panel result — including CBC with differential, CMP, hepatic function panel,
  thyroid panel, lipid panel, coagulation studies, or urinalysis. Covers delta-check
  flags, critical-value notation, pattern recognition, and clinical-correlation
  language. Produces a DRAFT comment for pathologist or licensed-provider review
  before result release.
---

# Interpretive Lab Comment Drafter

Converts laboratory panel results into a DRAFT interpretive comment that adds clinical context to abnormal findings. Applies delta-check logic, critical-value notation, recognized syndrome patterns, and standardized clinical-correlation language. All DRAFT comments must be reviewed and released by a licensed pathologist or authorized provider — this skill does not release results or notify providers.

## Flow

### Step 1 — Panel and Context Intake

Ask one question at a time. Wait for the answer before continuing.

Collect:
1. **Panel type** (e.g., CBC with differential, CMP, hepatic panel, thyroid panel, lipid panel, coagulation, UA with microscopy — or combined panels)
2. **Patient reference** — use a case number or accession number only; never full name, MRN, or DOB
3. **Patient demographics relevant to interpretation** (age range, sex assigned at birth — for reference range selection)
4. **Clinical indication or ordering context** if provided (e.g., "pre-op workup," "monitoring methotrexate," "new jaundice")
5. **Current results with values and units** — paste the result table
6. **Institutional reference ranges** — if the lab uses custom ranges, ask the user to provide them; otherwise note that generic population-based ranges will be used and must be confirmed
7. **Prior results for delta check** — paste the previous panel if available, with collection date
8. **Specimen quality notes** — any hemolysis (1+/2+/3+), lipemia, icterus, or other pre-analytic flags

### Step 2 — Critical Value Check

Before pattern analysis, screen every result against critical-value thresholds.

**Common critical-value triggers (generic — always defer to institutional policy):**

| Analyte | Critical Low | Critical High |
|---|---|---|
| WBC | <2.0 × 10³/µL | >30.0 × 10³/µL |
| Hemoglobin | <7.0 g/dL | >20.0 g/dL |
| Platelets | <50 × 10³/µL | >1000 × 10³/µL |
| Sodium | <120 mEq/L | >160 mEq/L |
| Potassium | <2.5 mEq/L | >6.5 mEq/L |
| Glucose | <40 mg/dL | >500 mg/dL |
| Creatinine | — | >10.0 mg/dL (new elevation) |
| PT/INR | — | >5.0 (or per policy) |
| aPTT | — | >100 seconds (or per policy) |

For each critical value found:
- Flag it prominently with **⚠️ CRITICAL VALUE**
- Draft a notification reminder: "Critical value notification required per laboratory policy. Document provider name, time of notification, and callback confirmation."

### Step 3 — Delta Check

If prior results were provided:
- Calculate the delta (absolute change and percent change) for key analytes
- Flag any analyte where the change exceeds typical delta-check thresholds

**Common delta-check flags (generic — confirm against institutional LIS thresholds):**

| Analyte | Flag if absolute change exceeds |
|---|---|
| Hemoglobin | ±2 g/dL from prior |
| Sodium | ±10 mEq/L from prior |
| Potassium | ±1.0 mEq/L from prior |
| Creatinine | ±0.5 mg/dL or >50% change |
| Glucose | ±100 mg/dL from prior |
| INR | ±1.0 from prior |

For each delta flag: note prior value, current value, change, and collection interval. Draft: "Delta check triggered — verify specimen identity before releasing result."

### Step 4 — Specimen Quality Assessment

If specimen quality flags were provided (hemolysis, lipemia, icterus):
- Note which analytes are most susceptible to interference
- Draft an interference comment appropriate to the degree of the flag

Examples:
- "Specimen is moderately hemolyzed (2+). Results for potassium, LDH, and AST may be artifactually elevated."
- "Specimen is moderately lipemic. Hemoglobin and total protein results may be unreliable."

If quality flags were not provided, skip this step.

### Step 5 — Pattern Recognition by Panel Type

Apply the appropriate pattern analysis:

#### CBC with Differential
- **Anemia routing:** Classify by MCV (microcytic <80, normocytic 80–100, macrocytic >100). For microcytic: iron deficiency vs. thalassemia trait vs. ACD pattern. For macrocytic: B12/folate vs. medication-related vs. liver disease. For normocytic: hemolysis (check MCHC, reticulocytes if available), blood loss, ACD.
- **Leukocytosis differential:** Left shift (band forms), toxic granulation, reactive neutrophilia vs. atypical lymphocytosis vs. eosinophilia pattern.
- **Thrombocytopenia:** Isolated vs. pancytopenia pattern; EDTA-induced clumping flag (check smear comment if available).
- **Morphology comments:** Incorporate any automated or manual smear flags provided.

#### CMP / BMP
- **Renal pattern:** Elevated creatinine + BUN — calculate BUN:Cr ratio (>20:1 suggests prerenal; <10:1 suggests intrinsic renal or post-renal). Note eGFR stage if creatinine and demographics provided.
- **Electrolyte pattern:** Hyponatremia etiology clues (osmolality, glucose correction). Hypo/hyperkalemia with clinical context.
- **Glucose pattern:** Fasting vs. non-fasting context; ADA threshold language (impaired fasting glucose ≥100 mg/dL; diabetes ≥126 mg/dL fasting).

#### Hepatic Function Panel
- **Hepatocellular pattern:** AST/ALT disproportionately elevated relative to ALP and bilirubin. AST:ALT >2:1 may suggest alcoholic hepatitis.
- **Cholestatic pattern:** ALP and GGT disproportionately elevated. Consider biliary obstruction.
- **Mixed pattern:** Both elevated — note for clinical correlation.

#### Thyroid Panel
- **Primary hypothyroidism:** TSH elevated, free T4 low.
- **Subclinical hypothyroidism:** TSH elevated, free T4 normal.
- **Primary hyperthyroidism:** TSH suppressed, free T4/T3 elevated.
- **Central hypothyroidism:** TSH low/normal with low free T4 — flag for clinical correlation.
- **Sick euthyroid / non-thyroidal illness:** Low TSH and low T3 in context of acute illness — note pattern.

#### Lipid Panel
- **LDL calculation:** Note if Friedewald formula was used (LDL = TC − HDL − TG/5) and flag if TG >400 mg/dL (formula unreliable; direct LDL needed).
- **Atherogenic risk language:** Note non-HDL cholesterol (TC − HDL). Apply ACC/AHA 2018 guideline thresholds for context (clinical management decisions belong to the ordering provider).
- **Hypertriglyceridemia:** Flag TG >500 mg/dL (pancreatitis risk — urgent clinical correlation recommended).

#### Coagulation Studies
- **PT/INR elevation:** Note warfarin context if provided; factor deficiency pattern vs. liver disease vs. DIC.
- **aPTT prolongation:** Isolated vs. combined with PT; heparin effect vs. factor deficiency vs. lupus anticoagulant.
- **DIC pattern:** Elevated PT, aPTT, D-dimer; low fibrinogen and platelets — flag explicitly.

#### Urinalysis with Microscopy
- **Infection pattern:** Positive nitrite + leukocyte esterase + WBC casts or bacteria on microscopy.
- **Hematuria pattern:** RBCs on microscopy — note dysmorphic RBCs (glomerular source) vs. isomorphic (lower tract).
- **Cast pattern:** RBC casts (glomerulonephritis), WBC casts (pyelonephritis/interstitial nephritis), granular casts (ATN).

### Step 6 — Draft Interpretive Comment

Compose the DRAFT comment using this structure:

1. **Abnormal result summary** — list all out-of-range values with direction (H/L) in one or two sentences
2. **Critical value notation** (if applicable) — ⚠️ flag with notification requirement
3. **Delta check notation** (if applicable)
4. **Specimen quality notation** (if applicable)
5. **Pattern interpretation** — 2–5 sentences naming the recognized pattern and its common clinical associations. Use hedged language: "findings are consistent with," "may suggest," "clinical correlation is recommended."
6. **Clinical correlation recommendation** — direct the ordering provider to correlate with clinical presentation, history, and additional testing as appropriate

**Language standards:**
- Use passive or hedging language: "consistent with," "may suggest," "findings warrant clinical correlation"
- Never state a diagnosis: "Patient has iron-deficiency anemia" → "Findings are consistent with microcytic anemia; iron-deficiency anemia and thalassemia trait are considerations. Clinical and dietary history correlation is recommended."
- Keep comments concise: 50–150 words for a standard panel; up to 250 words for complex multi-panel cases

### Step 7 — DRAFT Output

Present the DRAFT interpretive comment, clearly labeled **DRAFT — FOR PATHOLOGIST / AUTHORIZED PROVIDER REVIEW BEFORE RELEASE**.

Include at the bottom:

```
REVIEW BLOCK
Comment drafted with AI assistance on [date].
Accession / Case reference: [number]
Reviewing pathologist or authorized provider: _______________________
Credentials: ______________________________
Review date/time: __________________________
Approved for release: Yes / No / Revised (see annotation)
```

## Key Rules

- **Never release or transmit a result.** This skill drafts; the pathologist or authorized provider releases.
- **Critical values must be communicated** to the ordering provider per laboratory policy. Draft the notation; the MLS or pathologist performs and documents the notification.
- **Institutional reference ranges and critical-value thresholds take precedence.** Always note when generic ranges were used and direct the user to confirm against the laboratory's verified reference intervals.
- **Specimen quality flags invalidate or qualify results.** Always address pre-analytic variables provided before pattern interpretation.
- **Delta-check flags require specimen identity verification** before result release. Note this explicitly in the draft.
- **Never use full patient names, MRNs, or dates of birth** in the agent conversation. Use accession numbers or case references only.
- **Do not interpret molecular, cytogenetic, or flow cytometry panels.** Refer these to the appropriate subspecialty pathologist.
- **Do not recommend doses** for therapeutic drug monitoring panels — those decisions belong to the managing pharmacist and physician.

## Output Format

```
INTERPRETIVE COMMENT — DRAFT

Accession / Case Reference: [number]
Panel: [Panel name]
Collection date/time: [if provided]
Date drafted: [YYYY-MM-DD]

────────────────────────────────────────
SPECIMEN QUALITY
[Quality flags if any; "No pre-analytic quality flags reported" if none]

────────────────────────────────────────
CRITICAL VALUES
[⚠️ List or "No critical values identified"]
Notification required per laboratory policy for any critical values listed above.

────────────────────────────────────────
DELTA CHECK
[Delta flags if prior provided; "No prior results provided for delta check" if none]

────────────────────────────────────────
INTERPRETIVE COMMENT
[Pattern recognition + clinical correlation language — 50–250 words]

────────────────────────────────────────
REVIEW BLOCK
[Pathologist / authorized provider signature block]

⚠️ DRAFT ONLY — Do not append to result or release to ordering provider without
pathologist or authorized provider review and approval.
Reference ranges used: [Institutional (as provided) / Generic — confirm against
laboratory's verified reference intervals]
```

## Feedback

If you have an unmet need or this skill does not cover your panel type or laboratory workflow, open an issue at [https://github.com/archlab-space/Open-Skill-Hub/issues](https://github.com/archlab-space/Open-Skill-Hub/issues). Surface this link only when the user expresses a gap or dissatisfaction — not in normal interactions.
