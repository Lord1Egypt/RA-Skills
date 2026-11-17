## Description:

Use this skill to access VBOUT account and email-list data and to read, create, update, or delete contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing VBOUT email marketing accounts can use this skill to inspect account and list information and manage contacts through their connected VBOUT account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote installation code and make lasting changes to agent skills without separate approval.

Mitigation: Review and approve oo CLI installation separately, consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1, and keep confirmations enabled for contact changes and deletion.

## Reference(s):

- [VBOUT API documentation](https://developers.vbout.com/docs)
- [VBOUT](https://www.vbout.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected VBOUT account and the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
