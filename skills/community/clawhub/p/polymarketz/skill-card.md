## Description:

Comprehensive Polymarket prediction market skill for browsing trending markets, searching events, checking real-time odds and prices, viewing order books, analyzing market activity, tracking positions, and previewing wallet-gated trading commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zonder](https://clawhub.ai/user/zonder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to query Polymarket market data, inspect odds and order books, review public trader activity, and prepare trading actions from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet setup asks for a Polygon private key and stores it persistently on disk.

Mitigation: Do not use a funded wallet; use a fresh empty wallet for testing and rotate any key entered into this version before funding it.

Risk: The skill can surface market data and trading previews for real-money Polymarket activity.

Mitigation: Treat outputs as informational, review market details manually, and require explicit user confirmation before taking any external trading action.

Risk: Live trading, order viewing, and cancellation paths are incomplete and point users to additional authenticated CLOB tooling.

Mitigation: Review the code and required Polymarket authentication flow before relying on wallet-gated commands.

## Reference(s):

- [Polymarket](https://polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket Data API](https://data-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only commands can call public Polymarket APIs; wallet-related commands may read or write local wallet configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
