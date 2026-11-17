## Description:

Mpp Mobula lets agents fetch crypto prices, wallet positions, and market data through Mobula's pay-per-call MPP API using a Tempo wallet that pays per request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give agents pay-as-you-go access to Mobula crypto market-data endpoints without managing subscription API keys. It is suited to workflows that can safely manage a small funded hot wallet for per-call payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and uses funded crypto hot wallets, so host compromise or broad automatic invocation can expose funds.

Mitigation: Keep only very small balances in generated wallets, restrict which agents and users can trigger paid calls, and review the skill before installation.

Risk: Payment and private-key controls are broad for low-friction installation, especially if generic path calls are exposed to untrusted input.

Mitigation: Avoid exposing generic path calls to untrusted input, and prefer validation of request origin, endpoint prefix, currency, recipient, expiration, and cumulative spending before any transaction is signed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flotapponnier/skills/mpp-mobula)
- [Artifact README](artifact/README.md)
- [Artifact security model](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with bash and TypeScript examples; runtime calls return Mobula API data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a funded Tempo wallet for paid calls; normal outputs should not include private keys.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
