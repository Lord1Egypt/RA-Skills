## Description:

Google Apps Script: Upload local files to an Apps Script project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Google Workspace CLI commands for uploading local Google Apps Script source files to a target Apps Script project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command replaces all files in the target Apps Script project.

Mitigation: Verify the script ID and source directory before execution, and require user confirmation for the write operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-script-push)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and a target Apps Script project ID.]

## Skill Version(s):

1.0.2 (source: server release metadata; source skill metadata version: 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
