## Description:

Monitors China domestic refined fuel price adjustment windows and helps an agent answer current oil price and adjustment timing questions with reminder-style guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tengjunqing](https://clawhub.ai/user/tengjunqing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor China domestic fuel price adjustment windows, answer natural-language oil price questions, and prepare reminders before expected price changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitoring and memory storage may be enabled without clear user consent, limits, or an unsubscribe path.

Mitigation: Require explicit opt-in before scheduling reminders, set a check frequency and end date, and make memory entries and cron tasks reviewable and removable.

Risk: Fuel price data and adjustment forecasts can change quickly and may vary by region.

Mitigation: Refresh data from current sources for each answer, state whether figures are forecast or confirmed, and identify regional assumptions when reporting prices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tengjunqing/skills/oil-price-monitor)
- [Publisher profile](https://clawhub.ai/user/tengjunqing)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown-style natural-language responses with search queries, reminder templates, and optional cron configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Oil price values should be treated as time-sensitive and region-specific; predicted price movements should be clearly labeled as forecasts.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
