## Description:

Use this skill to read Censys certificate, host, and web property data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Censys account can retrieve certificate, host, and web property records through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may run downloaded installer code without a clear user checkpoint; the external installer and CLI were not validated by this artifact review.

Mitigation: Review and verify the CLI installation separately, and require approval before setup makes changes to the machine.

Risk: OOMOL intermediates Censys requests and manages the connected API key.

Mitigation: Use the connected account with awareness that requests and credentials are managed through OOMOL.

## Reference(s):

- [Censys API documentation](https://docs.censys.com/reference/get-started)
- [Censys](https://censys.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON results with shell command examples and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Censys asset retrieval; action inputs follow the connected service schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
