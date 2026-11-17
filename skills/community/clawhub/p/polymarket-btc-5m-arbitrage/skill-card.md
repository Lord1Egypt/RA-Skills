## Description:

Read-only Polymarket BTC 5-minute market scanner that reports candidate complementary-price edges; it never places orders, moves funds, or charges users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whh110112](https://clawhub.ai/user/whh110112)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can run this skill to scan public Polymarket BTC 5-minute Up/Down markets and manually review candidate complementary-price edges. It is trading-adjacent but does not place orders, move funds, persist data, or handle credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat observed candidate edges as profit guarantees or trading advice.

Mitigation: Treat scanner output as observations for manual review and account for fees, slippage, latency, partial fills, market rules, settlement disputes, regional requirements, and platform terms before acting.

Risk: Adding credentials or execution features would change the security posture of this read-only scanner.

Mitigation: Do not add private keys, API keys, wallet credentials, billing credentials, or automated order execution to this skill; build and review any trading executor separately.

## Reference(s):

- [Polymarket API read-only reference](references/api-reference.md)
- [BTC 5-minute candidate edge notes](references/trading-strategy.md)
- [ClawHub skill page](https://clawhub.ai/whh110112/skills/polymarket-btc-5m-arbitrage)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text status lines or pretty-printed JSON from the scanner, with Markdown guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market-data observations; continuous polling requires an explicit interval.]

## Skill Version(s):

1.0.2 (source: frontmatter, config.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
