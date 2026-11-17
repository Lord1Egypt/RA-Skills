## Description:

Professional T+0 intraday trading system for Chinese A-shares using Bayesian inference, Kelly criterion, VaR risk management, Tencent Finance quotes, position sizing, and automated monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang77160](https://clawhub.ai/user/yang77160)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Chinese A-share T+0 intraday trading opportunities, calculate risk and position sizing, monitor target prices, and produce trading guidance that should be independently verified before use with real money.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable trading recommendations that may be incorrect, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as educational signals only, verify market data and assumptions independently, and consult a qualified financial advisor before trading.

Risk: The scripts fetch live data from an external quote endpoint and may fail or return unexpected data.

Mitigation: Run in a virtual environment, validate quote results before relying on them, and avoid unattended decisions based on a single data source.

Risk: The HTML dashboard uses browser-loaded quote data patterns that the security evidence says should be avoided until fixed.

Mitigation: Do not use the dashboard for production monitoring unless the JSONP and dynamic HTML issues are remediated and reviewed.

Risk: Monitoring writes local log files and may create filesystem artifacts on the host.

Mitigation: Run as a normal user with limited permissions and review or change log paths before execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yang77160/skills/precise-t-trading)
- [Publisher profile](https://clawhub.ai/user/yang77160)
- [Skill documentation](artifact/SKILL.md)
- [Runtime requirements](artifact/requirements.txt)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q={code})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with quote summaries, risk calculations, trading decisions, alerts, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on live network access to Tencent Finance and local configuration such as stock code, share count, support level, and resistance level.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
