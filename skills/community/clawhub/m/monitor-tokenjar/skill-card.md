## Description:

Monitors the Uniswap TokenJar with a dashboard of balances, accumulation rates, burn economics, live deposit activity, and projected time to the next profitable burn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, protocol operators, and analysts use this skill to monitor Ethereum mainnet TokenJar balances, fee accumulation, profitability, and live deposit events without executing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release documentation includes unpinned install commands that can install code different from the reviewed artifact.

Mitigation: Install only from a pinned reviewed version or commit and avoid elevated privileges for changeable @latest or main-branch install sources.

Risk: Runtime permissions depend on the configured Uniswap MCP tools, even though the reviewed skill is intended for read-only monitoring and analysis.

Mitigation: Verify the Uniswap MCP permissions before use and confirm they are limited to public on-chain reads rather than wallet actions or transaction execution.

Risk: Profitability projections can be inaccurate because accumulation rates, token pricing, gas costs, and UNI price can change.

Mitigation: Treat projections as estimates, refresh the dashboard before acting, and review underlying balances, prices, and rates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/monitor-tokenjar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with formatted dashboard sections, live-feed updates, and alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports one-shot snapshots and streaming updates; projections depend on public on-chain data, token prices, accumulation estimates, and the configured streaming duration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
