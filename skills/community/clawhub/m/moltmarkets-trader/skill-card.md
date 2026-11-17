## Description:

Moltmarkets Trader helps agents screen MoltMarkets prediction markets, estimate probabilities, size positions with Kelly criterion, place bets, create and resolve markets, and track calibration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiceoogway](https://clawhub.ai/user/spiceoogway)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to analyze MoltMarkets prediction markets, prepare forecasting and position-sizing decisions, and run account, market creation, betting, and resolution workflows when properly authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live MoltMarkets account actions, including market creation, betting, and market resolution.

Mitigation: Require explicit confirmation before write actions, enforce clear spend limits, and prefer a dry-run mode before executing live scripts.

Risk: The security evidence reports unsafe argument handling in create-market-with-odds.sh.

Mitigation: Review and fix that script before use, especially before allowing automated market creation and seed betting.

Risk: Agents with access to the MoltMarkets API key can affect account balance and market state.

Mitigation: Install only in controlled agent environments with scoped secret access and review logs for write actions.

## Reference(s):

- [Forecasting Guide](references/forecasting-guide.md)
- [Kelly Criterion for MoltMarkets](references/kelly-criterion.md)
- [MoltMarkets API](https://api.zcombinator.io/molt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke live MoltMarkets API actions through shell scripts when an API key is present.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
