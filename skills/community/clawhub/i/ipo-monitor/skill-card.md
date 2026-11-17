## Description:

自动监控七大交易所IPO动态，比较本地历史记录，并将新增或更新的数据推送到飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qishenfeng-sys](https://clawhub.ai/user/qishenfeng-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Financial professionals, investment teams, and individual investors use this skill to monitor IPO activity across Chinese, Hong Kong, and U.S. exchanges and receive change alerts through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned or broadly ranged Python dependencies can reduce reproducibility across deployments.

Mitigation: Install in a virtual environment and pin reviewed dependency versions when repeatable production behavior matters.

Risk: IPO changes and alert text are sent to configured Feishu webhooks.

Mitigation: Use only approved Feishu webhook URLs and treat pushed messages as disclosed to that Feishu workspace.

Risk: Cron or daemon mode creates recurring background network activity and notifications.

Mitigation: Enable scheduled execution only when recurring monitoring is intended, and review logs and alert cooldown settings before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qishenfeng-sys/skills/ipo-monitor)
- [SKILL.md](artifact/SKILL.md)
- [SCHEDULER.md](artifact/SCHEDULER.md)
- [BROWSER_MIGRATION.md](artifact/BROWSER_MIGRATION.md)
- [Shanghai Stock Exchange IPO page](https://www.sse.com.cn/listing/renewal/ipo/)
- [Shenzhen Stock Exchange IPO page](https://www.szse.cn/listing/projectdynamic/ipo/)
- [Hong Kong Exchange newly listed securities](https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities)
- [NASDAQ IPO calendar](https://www.nasdaq.com/market-activity/ipos)
- [NYSE IPO calendar](https://www.nyse.com/ipo-center/ipo-calendar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration, Feishu message text, and local SQLite records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run once, in test mode, with browser-assisted scraping, or on a recurring cron/daemon schedule.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
