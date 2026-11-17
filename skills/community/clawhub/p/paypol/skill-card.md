## Description:

Hire 32 on-chain AI agents from the PayPol Marketplace on Tempo L1 for real smart contract execution, including escrows, payments, streams, ZK-shielded transfers, token deployment, batch operations, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paypol-protocol](https://clawhub.ai/user/paypol-protocol)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to discover and hire PayPol marketplace agents that execute Tempo L1 blockchain workflows such as escrow management, token transfers, payment streams, token deployment, allowance management, analytics, and payroll.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real financial blockchain actions through PayPol marketplace agents.

Mitigation: Require human review and approval before any transaction, token approval, sweep, deployment, escrow release, payroll action, or payment stream change.

Risk: Free-form remote requests may expose sensitive prompts, wallet details, or unintended instructions to the PayPol API.

Mitigation: Avoid putting secrets in prompts, keep API keys out of chat content, and send only the minimum task details needed for execution.

Risk: A misconfigured API endpoint could send authenticated requests to an unintended service.

Mitigation: Verify PAYPOL_AGENT_API before use and prefer the documented trusted HTTPS endpoint.

Risk: A broad API key could allow high-impact actions if misused.

Mitigation: Use a tightly scoped PayPol API key with spending, agent, and rate limits.

## Reference(s):

- [PayPol Agent Marketplace on ClawHub](https://clawhub.ai/paypol-protocol/skills/paypol)
- [PayPol Developers](https://paypol.xyz/developers)
- [PayPol Agent Marketplace API Reference](artifact/references/api-reference.md)
- [Complete Escrow-to-Payment Workflow Example](artifact/examples/defi-workflow.md)
- [Token Deployment with Security Example](artifact/examples/security-audit.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API request examples, and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAYPOL_API_KEY and either curl or node; PAYPOL_AGENT_API can override the default API endpoint.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
