## Description:

Google Apps Script: Upload local files to an Apps Script project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Developers and Google Workspace administrators use this skill to guide an agent through uploading local Apps Script source files to a specified Google Apps Script project with the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The push operation can overwrite every file in the target Google Apps Script project.

Mitigation: Confirm the script ID and source directory with the user before executing the command.

Risk: The skill depends on the local gws CLI and shared authentication setup.

Mitigation: Use it only in environments where the gws CLI installation and authentication context are trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/gws-apps-script-push)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI; the push command can replace all files in the target Apps Script project.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
