## Description:

Register domain names via crypto payments (USDC, USDT, ETH, BTC). Check availability, get pricing across 1000+ TLDs, and complete registration with on-chain stablecoin payments on Ethereum, Arbitrum, Base, or Optimism.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esokullu](https://clawhub.ai/user/esokullu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check domain availability, review pricing, and register domains after cryptocurrency payment. It is intended for workflows that need agent-guided domain registration with user-provided payment and registrant details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle OpenSRS management credentials that grant control over registered domains.

Mitigation: Use the skill only when credential handling in chat is acceptable, store received credentials in a password manager, and rotate or change domain management passwords after receipt.

Risk: Broad order-history queries may expose credentials or domain registration data that are not needed for the current task.

Mitigation: Query orders only when necessary and prefer domain-specific order lookups when investigating a particular registration.

Risk: The workflow depends on domain registration contact details and cryptocurrency payment references.

Mitigation: Confirm domain, pricing, chain, transaction hash, and registrant contact details with the user before registration.

## Reference(s):

- [LobsterDomains Homepage](https://lobsterdomains.xyz)
- [LobsterDomains API Keys](https://lobsterdomains.xyz/api-keys)
- [LobsterDomains Pricing](https://lobsterdomains.xyz/pricing)
- [ClawHub Skill Page](https://clawhub.ai/esokullu/skills/lobsterdomains)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON, markdown]

**Output Format:** [Markdown with inline shell commands, API request examples, and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LOBSTERDOMAINS_API_KEY environment variable and user-provided payment, transaction, contact, and domain details.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
