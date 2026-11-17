## Description:

Read and write Google Forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to inspect and issue Google Forms commands through the gws CLI for form creation, retrieval, updates, publish settings, responses, and watches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use configured Google Workspace credentials for Google Forms read and write operations.

Mitigation: Install only when that access is intended and review generated gws commands before execution.

Risk: Write operations such as batchUpdate or publish setting changes can alter business or sensitive forms.

Mitigation: Require human review before executing write commands against important forms.

## Reference(s):

- [Gws Forms on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-forms)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown command guidance with inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and configured Google Workspace credentials.]

## Skill Version(s):

1.0.12 (source: server release metadata; skill frontmatter metadata reports 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
