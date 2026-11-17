## Description:

Use this skill for Checkout.com requests to read, create, update, or delete customer data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support teams use this skill to manage Checkout.com customer records and linked payment instruments through an OOMOL-connected account. The instructions require confirmation before customer changes or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded installers without a separate approval or verification step.

Mitigation: Review and approve the CLI installation separately, including any automatic agent-skill changes.

Risk: Customer-data changes and deletion can affect customer records and linked payment instruments.

Mitigation: Use narrowly scoped Checkout.com access and retain user approval for customer changes or deletion.

## Reference(s):

- [Checkout.com API Reference](https://api-reference.checkout.com/)
- [Checkout.com](https://www.checkout.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas to shape request payloads.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
