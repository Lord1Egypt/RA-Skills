# Supplement Safety Gate

Run this gate before recommending or confirming supplements.

## Required inputs

- Current diagnoses
- Current medications
- Current supplements and doses
- Allergy history
- Pregnancy/breastfeeding status (if applicable)
- Kidney/liver concerns
- Main symptom or goal for taking each supplement

If required inputs are missing, mark result as `Needs clinician review`.

## Review checklist

## 1) Indication check

- Confirm each supplement has a clear goal.
- Remove "just in case" supplements without clear benefit.

## 2) Duplication check

- Detect overlapping ingredients across products.
- Flag duplicate fat-soluble vitamins and stimulant stacks.

## 3) Interaction check

- Check for potential interactions with prescribed meds.
- Check condition-level cautions (e.g., hypertension, arrhythmia, CKD, liver disease).
- If interaction risk is unclear, classify as `Needs clinician review`.

## 4) Dose and timing check

- Ensure dose is within commonly used conservative range.
- Align timing with meals/sleep/training to reduce side effects.
- Warn against escalating dose to compensate for missed doses.

## 5) Stop and escalate triggers

If any of the following appears, output `Avoid for now` and suggest medical follow-up:
- Prior severe adverse reaction
- Current severe symptoms possibly related to supplement use
- High-risk medication interaction
- Significant kidney/liver red flags

## Output format

Create a table with:
- Supplement
- Purpose
- Current dose/timing
- Risk flag
- Status (`Safe to continue` / `Needs clinician review` / `Avoid for now`)
- Action

Include a short note:
- "This is lifestyle guidance, not medical diagnosis. Confirm with a licensed clinician before major supplement changes."
