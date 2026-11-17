## Description:

Assesses whether a medical-device AI/ML change needs formal change control, classifies its severity, and returns a pass, hold, or reject verdict with reasons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

Apache 2.0

## Use Case:

Medical-device software developers, quality teams, and regulatory professionals use the skill to assess AI/ML changes against the LGD recorded, evidenced, and gated principles and prepare a traceable change-control judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain complete case details by default, which can expose sensitive device or patient-related information.

Mitigation: Use de-identified cases until full-context retention is disclosed and controllable.

Risk: A pass or go decision may be issued without the evidence checks the skill promises, and a result could be mistaken for deployment or regulatory approval.

Mitigation: Require qualified human review of every change-control decision; do not connect a positive result directly to deployment or regulatory approval. Correct the evidence checks and inconsistent verdict handling before relying on the results.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured verdict with change level, reasons, and evidence references; JSON is available from the bundled engine.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Citations and reasons for each LGD principle are intended parts of the judgment.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
