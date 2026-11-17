## Description:

Use the connected Kaleido account to list and inspect consortia, environments, nodes, and services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect the Kaleido consortia and infrastructure available to their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote installer code that has not been verified.

Mitigation: Review setup and use a verified, pinned oo CLI installation.

Risk: Setup can introduce broader agent changes without clear user control.

Mitigation: Disable unwanted agent-skill synchronization and connect Kaleido with read-only permissions.

## Reference(s):

- [Kaleido](https://www.kaleido.io)
- [Kaleido API documentation](https://api.kaleido.io/platform.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with shell commands and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account and resource data; shape depends on the selected action]

## Skill Version(s):

1.0.4 (source: frontmatter, server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
