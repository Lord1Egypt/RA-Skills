## Description:

Jarvis Stock Price helps agents look up real-time Shanghai and Shenzhen A-share stock prices with change, volume, and 5-day, 10-day, and 20-day moving averages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15910701838](https://clawhub.ai/user/15910701838)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Chinese A-share stock price data by ticker or name and present current price, change, volume, and moving-average context. Outputs should be treated as informational market data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock data and moving-average output could be mistaken for financial advice.

Mitigation: Present outputs as informational only and encourage users to verify data before making financial decisions.

Risk: The skill depends on an external @tdx-local provider that is not included in the artifact.

Mitigation: Confirm the provider is installed, trusted, and configured before using the skill.

Risk: The skill includes a disclosed upsell to a paid stock monitoring service.

Mitigation: Keep the free lookup behavior distinct from paid monitoring features and disclose the service boundary to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15910701838/skills/jarvis-stock-price)
- [Jarvis stock monitoring service](https://clawhub.ai/15910701838/jarvis-stock-monitor)

## Skill Output:

**Output Type(s):** [text, data]

**Output Format:** [Text or JSON-compatible stock quote fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ticker, name, price, change, change percent, volume, moving averages, and update time when data is available.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
