## Description:

Evaluates agent skill files against a Chinese-language SKILL-STANDARD-v3 checklist and returns quality scores, missing-file checks, and prioritized optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to inspect new or modified agent skills for metadata completeness, structure, referenced-file integrity, quality score, and concrete improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broader tool access than its current local audit scripts need, including Write permission.

Mitigation: Withhold or remove Write permission unless the user explicitly asks the agent to edit a skill, and run the scripts only on skill folders intended for inspection.

Risk: Missing referenced documentation can reduce the completeness of skill-audit guidance.

Mitigation: Review the included checklist and available scripts before relying on the report, and confirm any missing-reference findings against the target skill directory.

## Reference(s):

- [Skill Optimizer checklist](artifact/references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/lj22503/skills/lj22503-skill-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text containing checklists, scores, missing-file findings, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language audit output; scripts run locally against skill folders selected by the user]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
