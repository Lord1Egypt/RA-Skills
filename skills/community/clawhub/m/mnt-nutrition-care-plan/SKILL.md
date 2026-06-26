---
name: mnt-nutrition-care-plan
description: >
  Use this skill when a Registered Dietitian (RD/RDN), dietetic intern, or
  nutrition support team member needs to draft a Medical Nutrition Therapy (MNT)
  documentation note using the Nutrition Care Process (NCP) ADIME format. Covers
  nutrition assessment using the ABCDE framework, PES-statement diagnosis construction
  using IDNT terminology, individualized MNT intervention goals, and monitoring and
  evaluation parameters aligned to AND Evidence Analysis Library and CMS MNT benefit
  requirements. Produces a DRAFT ADIME note for licensed RD sign-off before entry
  into the medical record or submission to a payer.
---

# MNT Nutrition Care Plan Drafter

Converts patient intake data and clinical findings into a structured DRAFT Medical Nutrition Therapy note in ADIME format, aligned to the Academy of Nutrition and Dietetics (AND) Nutrition Care Process and Terminology (NCPT) and CMS MNT documentation requirements.

## Flow

### Phase 1 — Referral and Setting Intake

Ask the following, one group at a time. Tag each item as Confirmed / Assumed / Unknown.

1. Practice setting: acute care hospital, long-term care, outpatient clinic, home health, dialysis center, private practice, community health
2. Primary referral diagnosis (ICD-10-CM code preferred; plain-language description acceptable)
3. Secondary diagnoses relevant to nutrition (e.g., CKD stage, diabetes type, oncology diagnosis, wound/pressure injury)
4. Payer / billing context: Medicare Part B MNT benefit (HCPCS G0270/G0271 or G0108/G0109), Medicaid, commercial, self-pay — this determines note content requirements
5. Client case ID or pseudonym — never collect or record name, DOB, address, SSN, MRN, or other HIPAA-covered identifiers in this draft
6. Visit type: initial assessment or follow-up (reassessment); visit number in series
7. Referral source and reason for referral in referral party's own words

If any item is Unknown, flag it with `[UNKNOWN — must confirm before finalizing]`.

### Phase 2 — Nutrition Assessment (ABCDE Framework)

Collect and document findings across all five domains. Ask about each domain in turn.

**A — Anthropometrics**
- Current weight, height, BMI; weight history (usual body weight, % weight change over defined intervals)
- Edema present: yes / no; if yes — grade and location (adjust interpretation of weight)
- Amputation or other factor affecting standard weight interpretation: note and adjust
- Pediatric clients: weight-for-age, height-for-age, weight-for-height z-scores and percentiles

**B — Biochemical / Lab Data**
- Collect values and reference ranges. Flag values outside normal range.
- Priority labs by condition:
  - Diabetes: HbA1c, fasting glucose, eGFR
  - CKD / dialysis: BUN, creatinine, eGFR, potassium, phosphorus, calcium, bicarbonate, albumin/prealbumin (with interpretation caveat — acute-phase reactants)
  - Malnutrition / critical care: CRP, albumin, prealbumin, transferrin (interpret as inflammatory markers, not nutrition markers alone)
  - Cardiovascular: LDL-C, HDL-C, TG, total cholesterol
  - Wound / pressure injury: CBC, albumin, zinc, vitamin C
  - Oncology: CBC, albumin, weight trend

**C — Clinical / Physical Findings**
- Relevant nutrition-focused physical examination (NFPE) findings if performed: muscle wasting, fat loss, edema, skin/hair/nail signs, oral health, dentition, chewing/swallowing screen
- Current diet order or texture/liquid modification
- Feeding route: oral, enteral (tube type and location), parenteral (central/peripheral), combination
- Appetite: good / fair / poor; food aversions or preferences
- GI symptoms: nausea, vomiting, diarrhea, constipation, early satiety, dysphagia (if dysphagia: refer for SLP evaluation if not already completed)
- Food allergies and intolerances

**D — Dietary Intake**
- 24-hour recall, diet history, or food frequency — note method and limitations
- Estimated energy intake vs. requirement; estimated protein intake vs. requirement
- Fluid intake if relevant (CKD, heart failure, wound)
- Supplement use (vitamins, minerals, herbal, protein powders) — product name, dose, frequency

**E — Environmental, Social, and Functional Factors**
- Living situation, food access, cooking ability, financial constraints, cultural and religious food practices
- Functional status relevant to eating: independence, adaptive equipment needs, caregiver assistance
- Health literacy and readiness to change (Prochaska stage if applicable)

### Phase 3 — Nutrition Diagnosis (PES Statement)

Construct a PES statement using IDNT (International Dietetics and Nutrition Terminology) format:

> **[Nutrition Problem (P)]** related to **[Etiology (E)]** as evidenced by **[Signs and Symptoms (S)]**.

Rules for PES construction:
- P must be an AND NCPT-recognized nutrition diagnosis term (e.g., "Inadequate oral food/beverage intake," "Malnutrition," "Excessive fat intake," "Food-medication interaction," "Underweight," "Disordered eating pattern")
- E must be the most proximal, modifiable cause — something the RD can address through nutrition intervention
- S must include specific, measurable data points from the assessment (lab values, % weight change, intake percentage, etc.)
- Limit to one to three PES statements per note; prioritize the highest-acuity nutrition problem
- **Never** write a medical diagnosis (e.g., "Type 2 diabetes," "CKD") as the P — those are medical diagnoses, not nutrition diagnoses; they belong in the E or as context

Example (correct):
> Inadequate oral food/beverage intake related to decreased appetite secondary to chemotherapy as evidenced by 24-hour recall estimating 40% of estimated energy needs met and 8% unintentional weight loss over 4 weeks.

Example (incorrect — P is a medical diagnosis):
> Cancer related to chemotherapy as evidenced by weight loss.

### Phase 4 — Nutrition Intervention

For each PES statement, plan a corresponding intervention:

1. **Estimated requirements** (state method used):
   - Energy: kcal/kg, predictive equation (Mifflin-St Jeor, Penn State, Ireton-Jones), indirect calorimetry
   - Protein: g/kg — specify target range with clinical rationale
   - Fluid: mL/kg or mL/kcal if applicable
   - Micronutrient targets if clinically relevant (e.g., phosphorus restriction in CKD, potassium limit, sodium restriction in HF)

2. **MNT goals** — write as SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound). Example:
   - "Client will consume ≥75% of estimated energy needs by oral intake within 4 weeks, as reported on 3-day food record."

3. **Intervention strategy** — select applicable categories:
   - Nutrition education: topic, teaching method, materials provided
   - Nutrition counseling: approach (motivational interviewing, CBT-based, self-management support), behavior change target
   - Coordination of nutrition care: referral to food assistance programs, meal delivery, swallowing team, pharmacy
   - EN/PN prescription (if applicable): formula/solution, rate, advancement plan, monitoring parameters

4. **Barriers and facilitators** addressed in the plan

### Phase 5 — Monitoring and Evaluation

Define parameters that will measure progress toward each MNT goal:

| Parameter | Target | Measurement Method | Reassessment Timeframe |
|---|---|---|---|

Minimum parameters to include:
- Weight trend (frequency, goal direction)
- Relevant lab value(s) (specify target range)
- Dietary intake estimate vs. requirement
- Goal-specific behavior (e.g., carb counting accuracy, supplement adherence)

State the planned reassessment visit interval and billing code (if Medicare MNT: G0270 individual or G0271 group for follow-up; initial visit G0270 up to 3 hours in year 1 for CKD/DM).

### Phase 6 — DRAFT ADIME Note Assembly

Assemble a complete DRAFT note in ADIME format:

**A — Assessment**
[Synthesize ABCDE findings in narrative form. 2–4 sentences per domain as applicable.]

**D — Diagnosis**
[List PES statement(s). One per line.]

**I — Intervention**
[Estimated requirements, MNT goals (SMART), intervention strategy chosen.]

**M/E — Monitoring and Evaluation**
[Monitoring table. Reassessment date and billing code.]

**RD Attestation Block (unsigned placeholder):**
> RD/RDN Signature: __________________ Date: __________
> Credentials: __________________ NPI: ______________

Label the entire note:

> **DRAFT — For Licensed RD/RDN Review Only. Not Valid for Medical Record Entry or Payer Submission Until Signed.**

### Phase 7 — Gap and Quality Check

Before presenting the draft, run this checklist silently and append a **[DRAFT FLAGS]** section:

- [ ] All five ABCDE domains addressed or documented as Not Assessed with rationale
- [ ] PES statement uses AND NCPT-recognized nutrition diagnosis term
- [ ] PES E is modifiable through nutrition intervention
- [ ] PES S contains specific, measurable data from assessment
- [ ] MNT goals are SMART
- [ ] Monitoring parameters are defined with timeframes
- [ ] No direct patient identifiers in the note
- [ ] Payer documentation requirements met (Medicare MNT: reason for referral, diagnosis, goals)
- [ ] All Unknown items from Phase 1 flagged in context

## Key Rules

- **Never** record client name, DOB, address, SSN, MRN, or insurer ID in the draft. Use case ID or pseudonym only.
- **Never** write a medical diagnosis as the Nutrition Problem (P) in a PES statement.
- **Never** prescribe medications, supplements at pharmacological doses, or enteral/parenteral formulas without the supervising RD verifying the prescription against facility protocol.
- **Always** note when lab values are influenced by inflammation, hydration, or other confounders, and interpret accordingly.
- **Always** document when a standard equation is not validated for the client's population and note the limitation.
- **Always** require licensed RD/RDN review and signature before the note is entered in the medical record or submitted to a payer.
- Ask one group of questions at a time. Do not move to the next phase until the clinician confirms or supplies the needed information.

## Output Format

The final output is a structured Markdown DRAFT ADIME note followed by a **[DRAFT FLAGS]** checklist. The note must be ready for the supervising RD to review, edit, and sign without requiring additional data collection.

## Feedback

If a step in this workflow doesn't fit your practice setting's requirements or you encounter an unmet need, please raise it at the contribution link — but surface the link only when the user expresses dissatisfaction or an unmet need. Do not mention it in normal interactions.

The contribution link is: https://github.com/archlab-space/Open-Skill-Hub/issues
