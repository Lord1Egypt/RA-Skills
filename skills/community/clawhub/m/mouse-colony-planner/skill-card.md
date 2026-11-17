## Description:

Calculate breeding timelines and cage requirements for transgenic mouse colonies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to estimate breeding timelines, cage requirements, and costs for transgenic mouse colony planning from command-line parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculated timelines and costs are estimates and can be misleading when inputs are invalid or do not match local colony-management assumptions.

Mitigation: Validate numeric inputs before use and review outputs against lab protocols, animal-care constraints, and local cost schedules.

Risk: The requirements file lists unnecessary or unpinned dependencies for functionality that otherwise relies on Python standard-library modules.

Mitigation: Install in an isolated Python environment and remove or pin dependencies that are truly required before operational use.

## Reference(s):

- [Mouse Colony Planner on ClawHub](https://clawhub.ai/aipoch-ai/skills/mouse-colony-planner)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs estimated breeding phases, cage counts, costs, breeding pairs, and expected target-genotype mice.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
