## Description:

This skill lets agents inspect Workiom apps, lists, metadata, and records, and create records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Workiom can ask an agent to inspect connected apps, lists, metadata, and records, or create a record. The skill guides the agent to check the action schema first and obtain confirmation before writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated setup path can execute downloaded code without separate approval or clearly explaining broader local changes.

Mitigation: Install and verify a fixed CLI release separately, review or disable automatic skill synchronization, connect only the Workiom access needed, and retain approval for writes.

## Reference(s):

- [Workiom](https://workiom.com)
- [Workiom API Guide](https://help.workiom.com/article/workiom-api-guide)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill checks action schemas before constructing requests; writes require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
