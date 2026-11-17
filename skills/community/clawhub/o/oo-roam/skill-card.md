## Description:

Use Roam HQ through the oo CLI to retrieve groups, magicasts, and recordings, and to send messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to read Roam HQ groups, magicasts, and recordings, and to send messages through a connected Roam account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded installer code that was not inspected.

Mitigation: Review and approve the CLI installation separately before setup.

Risk: The CLI's automatic skill synchronization may make broader agent changes that this skill does not explain.

Mitigation: Review the synchronization behavior and consider the documented OO_SKILLS_SYNC_DISABLED control.

Risk: Roam requests pass through OOMOL, and sending a message changes Roam data.

Mitigation: Use a Roam account with appropriate access, understand the OOMOL connection, and confirm the exact message before sending.

## Reference(s):

- [Roam HQ API documentation](https://developer.ro.am/docs/roam-api)
- [Roam HQ](https://ro.am)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API calls, Text, Shell commands, Guidance]

**Output Format:** [Roam data returned as JSON and concise text summaries; oo CLI commands for actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results or a message sent to a Roam HQ group; writes require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
