## Description:

Checks material usage and loss tables for row-level arithmetic, total reconciliation, duplicate rows, and missing values, with each conclusion tied to source evidence; this free version runs the checks exposed by its bundled engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, project controls, and materials teams use this skill during monthly closing, reconciliation, or inventory review to check whether a material usage and loss table is arithmetically consistent and complete enough for a conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version does not perform every accounting check described around the skill, including amount equals issued quantity times unit price.

Mitigation: Review the runtime checks_given and checks_withheld lists for each run, and do not treat withheld checks as verified findings.

Risk: The skill is a Chinese-language local CLI for material usage and loss table checks, which can be misused if the operator cannot review the input and output language.

Mitigation: Use it only when the reviewer can understand the Chinese prompts, field names, findings, and insufficient-input messages.

Risk: Incomplete or unrecognized table input can otherwise lead users to overread the absence of findings.

Mitigation: Honor the insufficient_input status and provide the requested table headers and rows before drawing conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/material-usage-loss-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable CLI text or structured JSON containing executed checks, withheld checks, and findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally; reports checks_given and checks_withheld; returns insufficient_input instead of a conclusion when required table material is missing.]

## Skill Version(s):

1.0.53 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
