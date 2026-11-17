## Description:

Copies top World Cup traders on Polymarket using a Simmer-curated leader set and a daily rebalance flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-agent operators use this skill to generate and optionally execute a daily World Cup market copytrading plan based on Simmer-curated Polymarket leaders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute irreversible Polymarket trades using trading credentials.

Mitigation: Run in dry-run or sim mode first, then enable live Polymarket execution only after reviewing the generated plan and credential scope.

Risk: The SDK dependency is specified as a minimum version, so future unreviewed SDK code could run with trading credentials.

Mitigation: Pin or lock simmer-sdk to a reviewed version before allowing live Polymarket trades.

Risk: Copyability screening reduces slippage risk but does not remove market, leader churn, or thin-book risk.

Mitigation: Keep conservative max trade and slippage limits, retain leader-exit detection, and review live exposure after each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-worldcup-copytrader)
- [Skill documentation](artifact/SKILL.md)
- [Disclaimer](artifact/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text with optional JSON automaton status and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live Polymarket mode can place FAK, price-bounded trades when explicitly enabled.]

## Skill Version(s):

0.1.2 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
