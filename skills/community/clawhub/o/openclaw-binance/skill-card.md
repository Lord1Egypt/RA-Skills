## Description: <br>
Monitors Binance quantitative trading strategy data, analyzes performance, generates trading reports, and sends configured risk alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yibaig](https://clawhub.ai/user/yibaig) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading operators use this skill to monitor Binance trading pairs and strategy metrics, generate hourly or daily reports, and route risk alerts to configured notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store high-impact Binance API credentials. <br>
Mitigation: Use the minimum possible Binance API permissions, prefer read-only keys, disable withdrawals and trading unless verified as necessary, and apply Binance IP restrictions where possible. <br>
Risk: Credentials are stored in a local config.json file. <br>
Mitigation: Keep config.json out of version control and backups, and treat it as a secret-bearing file. <br>
Risk: Risk alerts are sent to a configured Feishu webhook. <br>
Mitigation: Verify the Feishu webhook destination before running so trading information is sent only to the intended channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yibaig/openclaw-binance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown reports, console status text, notification messages, and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under data/binance_trades and can send Feishu webhook alerts when configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
