## Description:

Audits Binance AI trading prompts, returns Pass/Warn/Block with guardrails, recommends permission handling, and can provide a safer prompt rewrite or share card URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto traders, developers, and operators use this skill to audit Binance automation prompts before granting account permissions, receive Pass/Warn/Block guidance, and generate safer operating guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw trading prompts and symbol lists are sent to a third-party Miraix service.

Mitigation: Do not include API keys, account identifiers, private portfolio details, or proprietary strategies unless the service's privacy and retention terms are acceptable.

Risk: The skill can be invoked implicitly without clear consent or data-minimization safeguards.

Mitigation: Confirm the prompt and symbol list before sending them to the external service, and minimize the submitted data to what is needed for the audit.

Risk: Permission plans and prompt rewrites may be mistaken for authorization to enable live trading permissions.

Mitigation: Treat the output as advisory and require human review before enabling Binance spot, futures, margin, transfer, or withdrawal permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richard7463/skills/miraix-binance-agent-firewall)
- [Miraix Binance Agent Firewall Audit API](https://app.miraix.fun/api/binance-agent-firewall)
- [Miraix Binance Agent Firewall Share Image API](https://app.miraix.fun/api/binance-agent-firewall/share-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with verdict, safety score, findings, permission plan, probation profile, safe rewrite, and optional share-card URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relies on Miraix public endpoints and Binance public market data; it does not claim private Binance account access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
