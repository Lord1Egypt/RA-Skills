## Description:

Pay Clawhub enables agents to discover pay-enabled services and execute operator-confirmed USDC payments on Base through the pay CLI for direct, tab, and x402 payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pay-skill](https://clawhub.ai/user/pay-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent find pay-enabled APIs, request paid resources, send direct USDC payments, manage metered tabs, and guide provider adoption of pay-gate when per-call payment support is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad wallet and paid-API authority.

Mitigation: Use only with explicit payment intent, require displayed final terms before payment, and set low per-call and tab limits.

Risk: Failed or repeated payment attempts can lead to duplicate or unintended charges.

Mitigation: Require a non-paying discovery or pricing check before pay requests, inspect payment errors, and never blind-retry failed payments.

Risk: Funding links and paid API request bodies can expose sensitive information to external services.

Mitigation: Treat funding links as sensitive, share them only after operator approval, and avoid sending sensitive request bodies to third-party APIs.

Risk: Installing an unverified payment CLI can expose wallet operations to supply-chain risk.

Mitigation: Install the CLI only from a verified pinned release before initializing or funding the wallet.

## Reference(s):

- [Pay Clawhub listing](https://clawhub.ai/pay-skill/skills/pay-skill)
- [Pay documentation](https://pay-skill.com/docs)
- [Rules](references/rules.md)
- [Errors](references/errors.md)
- [Tabs](references/tabs.md)
- [x402](references/x402.md)
- [Funding](references/funding.md)
- [A2A and AP2 Integration](references/a2a.md)
- [Discovery](references/discovery.md)
- [Provider Adoption](references/adoption.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pay CLI and ~/.pay/config.toml; payment actions should show final terms and wait for operator confirmation.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
