## Description:

Machine Payment Endpoint Preflight inspects one public HTTPS endpoint without credentials or payment, makes one bounded GET request, and reports whether its HTTP 402 x402 or MPP payment offers are parseable and internally consistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this workflow to preflight a public machine-payment endpoint before attempting any payment flow. It validates that the endpoint is safe to inspect, fetches it once without credentials, and summarizes payment-offer protocols, pricing, currencies, networks, recipients, expiries, conflicts, and the next safe action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable setup commands may install different helper skill versions over time.

Mitigation: Use OpenClaw or another trusted installer path with pinned versions where available, and review linked AgentPMT helper skills before installation.

Risk: Sensitive endpoint URLs or payment credentials could be exposed if provided during preflight.

Mitigation: Inspect only public HTTPS endpoints and do not provide private URLs, credentials, cookies, wallet keys, payment approval, or signing authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/machine-payment-endpoint-preflight)
- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/machine-payment-endpoint-preflight)
- [AgentPMT overview skill](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST setup skill](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Data Format Validation tool skill](https://clawhub.ai/agentpmt/data-format-validation)
- [Webhook - HTTP Request tool skill](https://clawhub.ai/agentpmt/webhook-http-request)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Compact Markdown report with machine-readable endpoint preflight fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers one public HTTPS endpoint per run and does not sign, pay, or broadcast transactions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
