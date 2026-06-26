---
name: model-card-drafter
description: >
  Use this skill when an ML engineer, data scientist, MLOps team, or responsible-AI
  lead needs to draft a Model Card for a machine-learning or AI model. Covers intended
  use, training data, evaluation metrics, disaggregated performance, limitations, and
  ethical considerations. Produces a DRAFT Model Card aligned to Google's Model Cards
  standard and EU AI Act technical documentation requirements for MLOps and governance review.
---

# Model Card Drafter

Converts a model description, training details, and evaluation results into a structured Model Card — the standard responsible-AI artifact for documenting a machine-learning model's intended use, performance, limitations, and ethical risks. Outputs a DRAFT for ML engineer and governance review before publication or regulatory filing.

## Flow

Ask one question at a time. Wait for the user's answer before proceeding to the next step.

### Step 1 — Model Identification

Collect:
- Model name and version
- Model type (e.g., binary classifier, multi-class classifier, regression, generative language model, object detection, embedding model)
- Organization or team responsible
- Date (or version date)
- License (if applicable)

### Step 2 — Intended Use

Collect:
- Primary intended use case (what task the model is designed to perform)
- Primary intended users (who will use the model and in what context)
- Out-of-scope uses (tasks or contexts for which the model must not be used)

Prompt the user: "Are there any use cases where this model should explicitly NOT be applied?" Record as a separate "Out-of-Scope Use" section.

### Step 3 — Training Data

Collect:
- Data sources (name, origin, collection method)
- Date range of training data
- Preprocessing and filtering steps applied
- Known data gaps, biases, or demographic imbalances in the training set
- Data licensing and consent status (public dataset, proprietary, licensed, synthetic)

If the user cannot describe training data: record as "Not disclosed" and flag as a documentation gap requiring resolution before publication.

### Step 4 — Evaluation Data

Collect:
- Test/evaluation dataset name and source
- Whether the evaluation set is held-out from training (must confirm)
- Known differences between evaluation data and real-world deployment data
- Data splits used (e.g., 80/10/10 train/val/test)

### Step 5 — Performance Metrics

Collect primary and secondary evaluation metrics (e.g., accuracy, F1, AUC-ROC, BLEU, precision, recall, RMSE, calibration).

Then collect disaggregated performance results: prompt the user to provide performance broken down by at least two subgroups relevant to the model's use (e.g., age group, gender, race/ethnicity, geography, language, income bracket, device type). If disaggregated results are not available, record as "Not yet evaluated" and flag as a high-priority gap.

### Step 6 — Ethical Considerations

Collect:
- Sensitive attributes the model processes or predicts (e.g., race, gender, health status, financial status)
- Known or anticipated disparate impacts across demographic groups
- Potential for misuse or harm if misapplied
- Privacy risks (does the model process or expose personal data?)
- Any fairness interventions applied during training or post-processing

### Step 7 — Limitations and Recommendations

Collect:
- Known failure modes or edge cases
- Performance degradation conditions (distribution shift, data quality issues, temporal drift)
- Conditions under which the model must not be deployed without additional review
- Recommended human oversight level (none / human-in-the-loop / human-on-the-loop / human-in-command)
- Recommended monitoring and re-evaluation cadence

### Step 8 — DRAFT Model Card Assembly

Assemble the DRAFT using the Output Format below. Label the document clearly:

```
DRAFT — Requires ML Engineer and Governance Review
Model Card Version: [version]
Date: [date]
```

Flag every field marked "Not disclosed" or "Not yet evaluated" with a `[DOCUMENTATION GAP — MUST RESOLVE BEFORE PUBLICATION]` annotation.

## Key Rules

- **Never** fabricate performance numbers, training data descriptions, or evaluation results not provided by the user.
- **Always** include a disaggregated performance section; if data is absent, flag it prominently.
- **Always** include an out-of-scope use section.
- **Always** label the output DRAFT and include a reviewer sign-off block.
- **Never** recommend publication or regulatory submission of a Model Card with unresolved documentation gaps.
- **Never** suggest a model is safe or unbiased without evidence from actual evaluation results.
- **Ask one question at a time**; do not present all fields as a single form unless the user explicitly requests batch input.
- If the model processes sensitive attributes (health, finance, criminal justice, employment), add a bolded **HIGH-SENSITIVITY USE CASE** flag at the top of the Ethical Considerations section.

## Output Format

Produce a structured Markdown document with the following sections in order:

```
# Model Card: [Model Name] v[Version]

**Status:** DRAFT — Requires ML Engineer and Governance Review
**Date:** [date]
**Organization:** [team/org]
**License:** [license or "Not disclosed"]

---

## Model Details

| Field | Value |
|-------|-------|
| Model name | |
| Version | |
| Model type | |
| Organization | |
| Date | |
| License | |

## Intended Use

**Primary intended uses:**
[description]

**Primary intended users:**
[description]

**Out-of-scope uses:**
[description]

## Training Data

**Sources:** [list]
**Date range:** [range]
**Preprocessing:** [description]
**Known biases or gaps:** [description]
**Licensing / consent:** [status]

## Evaluation Data

**Dataset:** [name and source]
**Held-out from training:** [Yes / No / Not confirmed — flag if not confirmed]
**Known distribution gaps:** [description]
**Splits:** [e.g., 80/10/10]

## Performance Metrics

**Primary metric:** [metric] = [value]
**Secondary metrics:** [list with values]

### Disaggregated Performance

| Subgroup | [Metric 1] | [Metric 2] |
|----------|------------|------------|
| [Group A] | | |
| [Group B] | | |

[DOCUMENTATION GAP — MUST RESOLVE BEFORE PUBLICATION] if missing.

## Ethical Considerations

**Sensitive attributes processed:** [list]
**Known disparate impacts:** [description]
**Potential for misuse:** [description]
**Privacy risks:** [description]
**Fairness interventions:** [description]

## Limitations and Recommendations

**Known failure modes:** [list]
**Performance degradation conditions:** [list]
**Deployment restrictions:** [list]
**Recommended human oversight level:** [level]
**Recommended re-evaluation cadence:** [cadence]

---

## Reviewer Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| ML Engineer / Model Owner | | | |
| MLOps / Governance Lead | | | |
| Responsible AI Reviewer | | | |

*This Model Card is a DRAFT. It must not be published, filed with regulators, or cited in external communications until all documentation gaps are resolved and all sign-offs are obtained.*
```

## Feedback

If this skill did not meet your needs or you encountered a workflow it does not cover, share your feedback at: https://github.com/archlab-space/Open-Skill-Hub/issues

Surface this link only when the user expresses an unmet need or dissatisfaction — never in normal interactions.
