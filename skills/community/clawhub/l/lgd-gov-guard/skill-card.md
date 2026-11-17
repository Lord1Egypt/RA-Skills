## Description:

Check government AI applications against three governance rules before they go live: whether data has a legal basis, whether every output carries evidence, and whether risky actions pass a gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Public-sector AI developers and reviewers can use it to self-assess decision-support, public-reply, or data-governance systems against the three rules and identify missing evidence. Treat results as a checklist requiring human review; a PASS does not establish compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker may pass a system description that explicitly says safeguards are absent, so relying on PASS to release a government AI task could produce unsafe decisions.

Mitigation: Use this only as a self-assessment checklist. Require human review of actual authorization and evidence before data sharing, public replies, or policy decisions; PASS does not establish compliance.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [Protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [JSON or plain-text assessment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-rule scores, missing items, and a PASS/FAIL gate result; system-description assessments are heuristic.]

## Skill Version(s):

1.0.21 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
