## Description:

Use ChaserHQ through an OOMOL-connected account to search and read customer, invoice, organization, and invoice-history data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve ChaserHQ customer, invoice, organization, status, and invoice-history information through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a remote installer without clear user approval.

Mitigation: Review and approve CLI installation separately; prefer a verified fixed release and disable startup skill synchronization when only ChaserHQ access is needed.

Risk: The connected account can expose sensitive customer and invoice information.

Mitigation: Use the connection only for authorized access to the intended ChaserHQ organization and data.

## Reference(s):

- [ChaserHQ](https://www.chaserhq.com/)
- [ChaserHQ API documentation](https://openapi.chaserhq.com/docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only customer, invoice, organization, status, and invoice-history data.]

## Skill Version(s):

1.0.4 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
