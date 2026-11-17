## Description:

Track and report multi-group stock portfolios with daily snapshots, live Yahoo Finance prices, P&L analytics, and push notifications for Feishu or Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stepuuu](https://clawhub.ai/user/stepuuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and portfolio operators use this skill to query grouped holdings, apply buy, sell, rebalance, fund, and cash updates, generate daily portfolio snapshots and reports, and optionally push reports to private notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup clones and installs an external engine repository that the skill relies on.

Mitigation: Review, pin, and verify the external repository before setup, and install dependencies inside an isolated project or virtual environment.

Risk: The skill can change financial records, including holdings, cash, fund balances, and deletion or overwrite operations.

Mitigation: Require explicit user confirmation before holding deletion, cash or fund overwrite, and report push operations; keep backups of portfolio data.

Risk: Webhook and bot tokens may send portfolio reports to external messaging services.

Mitigation: Scope Feishu and Telegram credentials to private destinations and avoid sharing tokens outside the configured environment.

## Reference(s):

- [Portfolio Daily Tracker on ClawHub](https://clawhub.ai/stepuuu/skills/portfolio-daily-tracker)
- [External engine repository referenced by setup script](https://github.com/Stepuuu/portfolio-daily-tracker.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON-backed portfolio data, and generated daily reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and mutate local portfolio holdings, snapshots, history CSV data, fund balances, cash balances, and optional notification settings.]

## Skill Version(s):

1.2.0 (source: frontmatter, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
