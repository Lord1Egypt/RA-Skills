## Description:

Generates a step-by-step plan to fix a GitHub issue from its title and description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinjin2024ux](https://clawhub.ai/user/jinjin2024ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, open source contributors, and bounty hunters use this skill to turn a GitHub issue title and description into a structured fix plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated plan may be generic because the skill does not inspect repository contents or validate the issue.

Mitigation: Review the plan against the target repository and issue context before implementing changes.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jinjin2024ux/skills/github-bounty-radar)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style plain text containing the issue title, ordered fix steps, and issue details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template-style plan generated from provided issue text; it does not inspect the repository or validate the issue.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
