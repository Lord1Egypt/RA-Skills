## Description:

Use when comparing live MLB win probabilities with executable prediction-market prices through Simmer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kvzsolt](https://clawhub.ai/user/kvzsolt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-tool operators use this skill to compare live MLB ESPN win probabilities with executable Simmer prediction-market prices, first in paper mode and only after explicit setup in live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Simmer API key and may read portfolio or position data.

Mitigation: Install only if that access is acceptable, and keep secrets in environment-managed storage rather than config files or logs.

Risk: Live mode can submit real-money prediction-market orders that may lose their full value.

Mitigation: Keep the skill in paper mode until validated, and use --live only with limits you are prepared to lose.

Risk: Multiple hosts using one account can fail to share one live risk ledger.

Mitigation: Use a shared SIMMER_MLB_STATE_PATH and one scheduler when multiple hosts or containers use the same account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kvzsolt/skills/mlb-live-trader)
- [ESPN MLB scoreboard API](https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard)
- [ESPN MLB summary API](https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/summary)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text with optional machine-readable JSON status lines and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; paper mode is default, while live trading requires explicit setup and --live.]

## Skill Version(s):

2.2.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
