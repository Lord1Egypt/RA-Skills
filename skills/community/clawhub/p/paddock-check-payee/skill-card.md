## Description:

Guides an agent to check an x402 payee wallet against Paddock's seller records before making a payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unblinkr](https://clawhub.ai/user/unblinkr)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to check a payee wallet against Paddock's seller records before paying a new x402 endpoint or accepting changed payment terms. It tells the agent when to block a mismatched payee and when to warn the user or proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a payee shares the x402 resource URL and payment terms with Paddock.

Mitigation: Use only when sharing those details is acceptable; adopt an explicit policy or self-hosted alternative for sensitive payment relationships.

Risk: An unknown result, unavailable response, error or usage-limit response does not block payment.

Mitigation: For payments that require verified payees, require a separate approval or verification step before paying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/unblinkr/skills/paddock-check-payee)
- [Paddock check_payee MCP server](https://paddock.finance/api/mcp/mcp)
- [Paddock API access](https://paddock.finance/api-access)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the check outcome and, for a failed check, the reasons and full_check link when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
