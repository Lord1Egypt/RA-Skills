## Description:

Dry-run Kalshi skill that finds politics-related markets, picks a valid candidate at random, runs Simmer context checks, and proposes a trade plan without placing a real order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skybinjf](https://clawhub.ai/user/skybinjf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Kalshi politics markets and generate a manual-review trade plan using Simmer market context and bankroll-aware sizing. It is intended for planning only; it does not place live orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package schedules recurring credentialed runs every 30 minutes.

Mitigation: Remove the cron automaton or explicitly opt into it only after reviewing the run cadence and expected account activity.

Risk: The skill requires a Simmer API key and can perform Simmer-side market indexing during planning.

Mitigation: Use a narrowly scoped, revocable Simmer key and rotate or revoke it after testing.

Risk: The skill depends on the external simmer-sdk package for market context and sizing behavior.

Mitigation: Pin or audit the SDK version before installation and review generated plans before taking any live trading action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skybinjf/skills/kalshi-politics-random-buyer)
- [ClawHub publisher profile](https://clawhub.ai/user/skybinjf)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text with a JSON execution_plan object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and optional environment variables for search terms, price bounds, edge threshold, slippage threshold, and random seed.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
