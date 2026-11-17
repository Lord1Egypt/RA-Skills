## Description:

Trades the highest-edge active AION Polymarket market matching a query using a user-supplied fair probability, AION context safeguards, and Kelly-style sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to scan active Polymarket markets, compare prices against a supplied fair probability, and produce dry-run or explicitly authorized live trade decisions with AION safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit signed Polymarket orders when live mode and signed order data are provided.

Mitigation: Use dry-run mode unless live trading is intended, scope AION credentials narrowly, and provide signed orders only for reviewed trades.

Risk: A custom AION_BASE_URL changes the endpoint that handles credentials, market data, and order-related payloads.

Mitigation: Use the default or another fully trusted endpoint, and review endpoint changes before deployment.

Risk: Scheduled or daemon execution can repeatedly evaluate markets and auto-redeem positions.

Mitigation: Run in an isolated environment, monitor operator summaries, and keep stake, slippage, Kelly multiplier, and polling settings conservative.

Risk: The SDK dependency is unpinned while handling credentials and signed orders.

Mitigation: Pin and review dependency versions in deployment environments before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fivegive249-ship-it/skills/polymarket-edge-trader)
- [AION agents portal](https://pm-t1.bxingupdate.com/agents)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain-text operator summaries with command examples and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires explicit --live execution with wallet and signed-order inputs.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
