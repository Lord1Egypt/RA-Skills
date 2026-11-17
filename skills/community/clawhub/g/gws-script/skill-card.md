## Description:

Manage Google Apps Script projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to discover and invoke gws CLI commands for Google Apps Script processes, projects, deployments, versions, and script execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Apps Script project update operations can replace existing project files.

Mitigation: Have the agent inspect the gws schema, confirm the target project, and retrieve or back up existing content before using projects.updateContent or the push helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-script)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI; agents should inspect gws schema output before building command parameters.]

## Skill Version(s):

1.0.2 (source: server release metadata; internal skill metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
