## Description:

Sender (sender.net). Use this skill for ANY Sender request — reading, creating, updating, and deleting data. Whenever a task involves Sender, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read Sender campaigns, groups, subscribers, fields, and workflows, and to create or update subscriber data and group membership through a connected Sender account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded installer code, and the installer contents and exact installed CLI version were not verified.

Mitigation: Review the installer and use a reviewed, fixed CLI version before installation.

Risk: The CLI may synchronize changes to installed agent skills at startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable the documented startup synchronization.

Risk: Sender subscriber data is processed through OOMOL, and account changes can affect live records.

Mitigation: Assess OOMOL's data handling and retain the required approvals before making account changes.

## Reference(s):

- [Sender API documentation](https://api.sender.net/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Sender](https://www.sender.net)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are checked before calls; write and destructive actions require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
