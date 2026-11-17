## Description:

Analyzes preclinical pharmacokinetic/pharmacodynamic concentration-time data and reports PK parameters with explicit assumptions and reviewable outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and preclinical research teams use this skill to calculate and report PK parameters from concentration-time data for workflows such as IND-enabling studies, dose selection, and drug candidate ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies are declared without pinned versions.

Mitigation: Install and run the skill in a virtual environment or container, and pin reviewed versions of numpy and scipy before regulated or decision-critical use.

Risk: Input CSV files may contain unintended, malformed, or unsupported PK/PD data.

Mitigation: Provide only intended concentration-time CSV files and review assumptions, units, and fit quality before using the output.

Risk: Generated PK/PD results are computational assistance, not validated clinical or regulatory conclusions.

Mitigation: Have qualified domain reviewers verify outputs before using them for clinical, regulatory, or program decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/preclinical-pkpd-analyst)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with optional shell commands and text PK parameter reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports assumptions, constraints, risks, unresolved items, and validation needs when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
