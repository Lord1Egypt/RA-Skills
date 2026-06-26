## Description: <br>
港股+A股实时盯盘系统，支持技术分析、涨跌幅告警、飞书推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merlini0116](https://clawhub.ai/user/merlini0116) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor selected Hong Kong and A-share equities, generate technical-analysis reports, and send threshold-based market alerts through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded QVeris key and a fallback path that can pass it to an external data-source helper. <br>
Mitigation: Remove the embedded key, rotate it if it was usable, and require installers to provide their own QVERIS_API_KEY before enabling QVeris fallback. <br>
Risk: The artifact includes a preset Feishu chat ID, so alerts may be sent to a destination the installer did not choose. <br>
Mitigation: Replace the Feishu chat ID with the installer's own destination or disable Feishu messaging before running monitor or alert scripts. <br>
Risk: Cron examples and generated data/report directories can keep monitoring and storing market data after the user expects it to stop. <br>
Mitigation: Review cron entries, generated data paths, report paths, and retention settings during installation and removal. <br>
Risk: Custom stock codes and generated trading guidance may be incorrect or stale. <br>
Mitigation: Validate stock symbols and treat generated analysis as monitoring support, not financial advice. <br>


## Reference(s): <br>
- [股票配置参考](references/stocks.md) <br>
- [ClawHub skill page](https://clawhub.ai/merlini0116/hk-stock-monitor) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown reports, Feishu alert messages, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads market data from Sina Finance with QVeris fallback, writes local JSON history and Markdown reports, and can send Feishu alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
