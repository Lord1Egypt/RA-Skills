## Description:

Search and read Dixa agents, conversations, end users, messages, and presence through a connected Dixa account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and agents use this skill to retrieve Dixa agent, conversation, end-user, message, and presence data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can execute downloaded installer code and make lasting local agent changes.

Mitigation: Use a reviewed, version-pinned CLI installation, and require approval before a Dixa request triggers software installation.

Risk: Dixa access is mediated by OOMOL, while the hosted connector internals remain unverified.

Mitigation: Review the Dixa connection and grant only the access needed for the requested tasks.

## Reference(s):

- [Dixa API documentation](https://docs.dixa.io/)
- [Dixa](https://www.dixa.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Retrieved Dixa data as JSON with concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented retrieval of Dixa records and presence information.]

## Skill Version(s):

1.0.4 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
