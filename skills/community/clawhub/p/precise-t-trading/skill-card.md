## Description: <br>
Professional T+0 intraday trading system for Chinese A-shares that uses Bayesian inference, Kelly criterion position sizing, VaR risk management, Tencent Finance quotes, and automated monitoring to support intraday trading decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang77160](https://clawhub.ai/user/yang77160) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-tool developers use this skill to analyze Chinese A-share T+0 opportunities, calculate risk-aware position sizing, monitor prices, and produce trading-support outputs. Recommendations should be independently checked before any real-money use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce actionable trading guidance from simulated and hard-coded inputs. <br>
Mitigation: Use it for education or paper trading until mock and hard-coded inputs are replaced with verified market and trade-history data, and independently verify every recommendation. <br>
Risk: Monitoring behavior may write logs to a hard-coded location. <br>
Mitigation: Review the log path before running the monitor and avoid running the skill with administrator privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang77160/precise-t-trading) <br>
- [Publisher profile](https://clawhub.ai/user/yang77160) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q={code}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script-generated text, HTML dashboard files, and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch Tencent Finance quote data and may write monitoring logs when the monitor script is used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
