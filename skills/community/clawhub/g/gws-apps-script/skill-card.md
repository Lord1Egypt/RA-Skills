## Description:

Google Apps Script: Manage and execute Apps Script projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect, manage, execute, and update Google Apps Script projects through the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The projects.updateContent method can clear existing files in a Google Apps Script project.

Mitigation: Confirm the target project and keep a backup or source-controlled copy before using updateContent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-apps-script)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and CLI parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and Google Workspace authentication context from the shared gws skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
