## Description:

Provides rubric-weighted contest scoring and a structured JSON report to support, not replace, human judges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Contest organizers and judges use the skill to calculate weighted rubric scores and review a structured scoring report. Final adjudication remains with human judges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The declared tool access is broader than the scoring task requires, and the documentation conflicts on whether local code runs.

Mitigation: Review before installation; remove unneeded WebFetch and Write access, align file and subprocess permissions with actual use, and clarify whether to run the CLI.

Risk: Missing scores are counted as zero, and the cited judging rules and grade thresholds are not yet verified.

Mitigation: Supply complete rubric inputs, verify the current contest rules and thresholds, and have human judges review results before decisions.

## Reference(s):

- [ClawHub release listing](https://clawhub.ai/zhaoxinghua09-cell/skills/judging-rubric-grader)

## Skill Output:

**Output Type(s):** [JSON scoring reports, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes weighted totals, grades, per-dimension scores, warnings, and a result code; incomplete scores are counted as zero.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; package documentation says 1.1.1 and script says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
