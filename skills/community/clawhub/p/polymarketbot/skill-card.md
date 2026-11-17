## Description:

Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redrepz](https://clawhub.ai/user/redrepz)

### License/Terms of Use:


## Use Case:

External users and trading automation developers use this skill to monitor and trade Polymarket crypto fast markets with CEX momentum signals, starting in dry-run mode and optionally executing live trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real Polymarket trades when run with live trading enabled.

Mitigation: Run in dry-run mode first, use small position sizes and daily budgets, and enable live trading only after reviewing the strategy and wallet permissions.

Risk: Wallet and API credentials are required for live operation.

Mitigation: Use a dedicated wallet with limited funds, store credentials only in the intended environment, and avoid broadly exposing WALLET_PRIVATE_KEY.

Risk: The release depends on an unpinned trading SDK.

Mitigation: Pin and review the simmer-sdk dependency before live or scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redrepz/skills/polymarketbot)
- [Publisher profile](https://clawhub.ai/user/redrepz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON automaton summaries when run in managed mode.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
