## Description:

Help Scout (helpscout.com). Use this skill for ANY Help Scout request — reading, creating, updating, and deleting data. Whenever a task involves Help Scout, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams use this skill to read and manage Help Scout customer records and conversations through their connected account. It can retrieve information and carry out approved conversation or customer updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified software and automatic skill synchronization can make broader agent changes without clear user approval.

Mitigation: Review and approve the oo CLI installation separately, preferably using a pinned, verified release. Check its automatic skill synchronization settings before use, and retain the skill's confirmations for write and destructive actions.

Risk: Using the connected service involves Help Scout customer data handled through OOMOL.

Mitigation: Assess whether OOMOL is an appropriate handler for the account's customer data before connecting or using the skill.

## Reference(s):

- [Help Scout](https://www.helpscout.com)
- [Help Scout Mailbox API documentation](https://developer.helpscout.com/mailbox-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Shell commands, Guidance]

**Output Format:** [JSON action payloads and responses, with text summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
