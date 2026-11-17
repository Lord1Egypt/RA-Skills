## Description:

Automatic parameter optimizer for polymarket-executor that reads performance metrics every 6 hours, analyzes win rates and P&L by strategy, adjusts learned_config.json, builds paper-trade metrics, and assesses live trading readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading-system operators use this skill to tune Polymarket executor parameters from local paper-trade and portfolio performance data. It writes updated strategy thresholds, allocation settings, Kelly sizing, scan frequency, and optimization logs for later executor runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optimizer can automatically change trading configuration that affects future strategy thresholds, allocations, Kelly fraction, and scan frequency.

Mitigation: Run it with a dedicated minimal environment, review generated learned_config.json before live trading, and keep backups so configuration changes can be rolled back.

Risk: Telegram reports may contain portfolio and strategy performance data.

Mitigation: Verify TELEGRAM_CHAT_ID and bot configuration before enabling reports, and avoid sharing the bot token or reports outside the intended channel.

Risk: Persistent scheduling can run the optimizer unattended with broad local file access.

Mitigation: Prefer a least-privilege scheduler or container user, avoid the root systemd setup when possible, and monitor optimizer_log.jsonl for unexpected changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/polymarket-optimizer)
- [Polymarket Optimizer repository](https://github.com/georges91560/polymarket-optimizer)

## Skill Output:

**Output Type(s):** [Configuration, JSON files, Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON configuration and JSONL log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update learned_config.json, append optimizer_log.jsonl, build performance metrics from paper trades, and optionally send Telegram summary reports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
