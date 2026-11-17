## Description:

A guide for building a multi-bot arbitrage coordination framework with marketplace discovery, escrow protection, trust verification, cross-exchange opportunity detection, execution verification, profit splitting, MEV protection, and audit trails.

This skill is for research and development only.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and prototype coordinated arbitrage bots that discover counterparties, negotiate terms, use escrow-backed settlement, verify execution, and produce audit trails. Because the release evidence flags financial settlement and sensitive trading-signal risks, use should remain in sandbox or paper-trading environments until controls are independently reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The framework handles financial settlement and sensitive trading signals with material confidentiality and verification gaps.

Mitigation: Use recipient-scoped or encrypted event delivery, verify reporter identities and signatures before settlement, and avoid exposing opportunity details beyond the counterparties that need them.

Risk: Raw exported signing keys can expose agent identity and settlement authority.

Mitigation: Store signing keys in a secrets manager or hardware-backed key store, rotate compromised keys, and avoid logging or committing AGENT_SIGNING_KEY values.

Risk: Real-money arbitrage can create execution, counterparty, exchange, and regulatory risk.

Mitigation: Test only in paper-trading or sandbox environments until exchange adapters, financial controls, and compliance obligations are independently reviewed.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/mirni/skills/greenhelix-bot-arbitrage-framework)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API Reference](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python examples, curl commands, configuration notes, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AGENT_SIGNING_KEY environment variable for signing examples; the artifact is non-executable and installs no dependencies.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
