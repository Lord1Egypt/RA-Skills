## Description:

Learn about Moralis and Web3 development, answer exploratory questions, and route users to the appropriate Moralis Data API or Streams skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novnski](https://clawhub.ai/user/novnski)

### License/Terms of Use:

MIT

## Use Case:

Developers and Web3 builders use this skill to understand Moralis capabilities, pricing, supported chains, and when to use Moralis Data API versus Streams. It provides onboarding guidance and points users toward the appropriate technical skill for wallet, token, NFT, DeFi, analytics, or real-time event use cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moralis pricing, chain support, or product capabilities may change after the bundled references are published.

Mitigation: Verify commercial decisions against the current Moralis documentation and account dashboard before relying on the guidance.

Risk: Users may expose API keys while moving from onboarding guidance to technical Moralis skills.

Mitigation: Store API keys in environment files or secret managers and avoid pasting secrets into chat unless that is an intentional, controlled workflow.

Risk: Webhook or trading-bot workflows can act on duplicate, delayed, or unsafe event signals.

Mitigation: Add application-level safety controls, idempotent webhook handling, and human review before deploying automated trading or alerting behavior.

## Reference(s):

- [Moralis Documentation](https://docs.moralis.com)
- [Moralis Onchain Skills Repository](https://github.com/MoralisWeb3/onchain-skills)
- [Learn Moralis ClawHub Listing](https://clawhub.ai/novnski/skills/learn-moralis)
- [Moralis Frequently Asked Questions](references/FAQ.md)
- [Moralis Product Comparison](references/ProductComparison.md)
- [Moralis Use Case Implementation Guide](references/UseCaseGuide.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown conversational guidance with inline references to related skills and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Knowledge-only output; does not execute code or call Moralis APIs directly.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
