## Description:

A China-market gold monitoring skill that runs a Python dashboard for domestic gold ETFs, Shanghai Gold Exchange AU9999 spot prices, COMEX gold futures, the U.S. Dollar Index, USD/CNY, and A-share gold mining stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[song0828](https://clawhub.ai/user/song0828)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents supporting China-market gold investors use this skill to run an informational dashboard and compare gold ETF, spot gold, futures, currency, and mining-stock signals. The output is for monitoring and analysis support only, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market prices can be delayed, unavailable, or inconsistent because the dashboard depends on third-party data through akshare.

Mitigation: Verify prices against an authoritative market data source before making financial or trading decisions.

Risk: The dashboard presents market interpretation that could be mistaken for investment advice.

Mitigation: Treat the output as informational analysis support only and apply independent judgment before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/song0828/skills/gold-monitor-cn)
- [ClawHub publisher profile](https://clawhub.ai/user/song0828)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Console text with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and third-party market data access through akshare; values may be delayed or unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
