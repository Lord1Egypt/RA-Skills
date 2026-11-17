## Description:

Deterministic handbook-grounded retrieval and thermocouple computations for reflow profile compliance outputs such as ramp, TAL, peak, feasibility, and selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing process engineers and developers use this skill to extract handbook constraints and calculate reflow profile compliance metrics from thermocouple and MES data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handbook, MES, thermocouple, or defect datasets may contain sensitive manufacturing information.

Mitigation: Confirm those datasets are approved for agent access before using the skill.

Risk: Incorrect handbook extraction or missing thermocouple data could lead to misleading compliance conclusions.

Mitigation: Review handbook-derived configuration values, emit nulls for unavailable metrics, and avoid claiming pass status when required data is missing.

Risk: Non-monotonic timestamps or duplicate samples can distort ramp and time-above-liquidus calculations.

Mitigation: Sort samples by run, thermocouple, and time, and ignore segments where elapsed time is not positive.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets and JSON-compatible output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic calculations use sorted IDs, stable sensor tie-breaks, rounded finite numeric values, and nulls for missing data.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
