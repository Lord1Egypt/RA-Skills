## Description:

Read, create, and update Salesflare accounts, contacts, opportunities, and tasks through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to retrieve and manage Salesflare CRM records through their connected OOMOL account. It requires confirmation before record changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-tool setup fallback can trigger a CLI installation, and the connector's access to CRM data and documented skill-sync behavior were not fully verified.

Mitigation: Review and approve the CLI installation separately before using the fallback, consider OOMOL's CRM access and skill-sync behavior, and keep confirmations for record changes.

## Reference(s):

- [Salesflare](https://salesflare.com)
- [Salesflare API documentation](https://api.salesflare.com/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [oo CLI commands with JSON payloads and Salesflare connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Record-changing actions require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
