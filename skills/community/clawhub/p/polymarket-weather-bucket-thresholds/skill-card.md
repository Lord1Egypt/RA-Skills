## Description:

Global temperature bucket threshold strategy via Simmer. Buy YES under 15%, sell full position at 45%, max ~$2 entries, max 5 trades/scan, every 2 minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oxsnosh](https://clawhub.ai/user/oxsnosh)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to run a Simmer-based weather market threshold strategy that buys YES below 15% probability and exits YES positions at 45% or above. It is dry-run by default and requires explicit live-mode enablement for trading actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform account-level trading actions when live mode is enabled.

Mitigation: Review before enabling live mode and keep dry-run mode until trading scope, account permissions, and loss limits are confirmed.

Risk: Exit logic may affect positions beyond those opened by this skill.

Mitigation: Tighten exits so they only sell positions that can be attributed to this skill before live deployment.

Risk: Trading controls are described as too loose for account-level actions.

Mitigation: Hard cap entry spend and total trades, block on any context warning, and pin or remove the unused dependency before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oxsnosh/skills/polymarket-weather-bucket-thresholds)
- [Simmer API endpoint](https://api.simmer.markets)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration instructions]

**Output Format:** [Console text with JSON-like dry-run payloads and live API trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; default dry-run mode prints trade payloads instead of submitting live trades.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
