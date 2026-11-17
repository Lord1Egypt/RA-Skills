## Description:

Helps authenticated users inspect Mermail Agent Wallet balances, arrange funding and signing handoffs, and request authorized PayBox transfers, swaps, USDC bridge approvals, and isolated x402 payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet users and their agents use this skill to check balances, plan funding, preview user-directed transfers, swaps and USDC bridges, make isolated x402 payments, and track approval or settlement status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet access and financial operations require a full-profile Mermail MCP OAuth connection.

Mitigation: Connect only when wallet features are needed, and review wallet grants and PayBox approval settings before use.

Risk: Autonomous approval can submit exact user-authorized operations without another Mermail approval prompt.

Mitigation: Review autonomous grants carefully; preview the precise asset, chain, amount, destination and spending cap before each write.

Risk: Untrusted messages or paid-service content could introduce payment terms the user did not authorize.

Mitigation: Take payment authority only from the authenticated user's current request and require confirmation for missing or changed terms.

Risk: Pending or uncertain transaction outcomes can cause duplicate payments if retried.

Mitigation: Check the original request status and do not retry an uncertain wallet write.

## Reference(s):

- [Mermail AI skills documentation](https://docs.mermail.app/ai/skills)
- [ClawHub skill release](https://clawhub.ai/mermail/skills/mermail-agent-wallet)
- [Wallet workflows](references/workflows.md)
- [Wallet tool map](references/tools.md)
- [Wallet security boundary](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with transaction previews, handoff links, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include one first-party console handoff URL; pending requests are not reported as settled.]

## Skill Version(s):

1.0.19 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
