## Description:

BTCPay Server (btcpayserver.org). Use this skill for ANY BTCPay Server request — reading, creating, and updating data. Whenever a task involves BTCPay Server, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to read BTCPay Server stores and invoices, create invoices, or update invoice status and metadata through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unverified CLI installer or introduce broader persistent changes to agents.

Mitigation: Use a reviewed, verified CLI release and disable additional skill synchronization if it is unwanted.

Risk: The connected account can make invoice changes.

Mitigation: Connect only the permissions needed and retain confirmation for invoice changes.

## Reference(s):

- [BTCPay Server](https://btcpayserver.org)
- [BTCPay Server Greenfield API documentation](https://docs.btcpayserver.org/API/Greenfield/v1/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-btcpay-server)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and operational guidance; action responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields depend on the selected BTCPay Server action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
