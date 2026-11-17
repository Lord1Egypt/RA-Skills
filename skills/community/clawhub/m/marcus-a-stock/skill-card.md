## Description:

Generates daily A-share momentum reports with market stance, watchlists, position sizing guidance, and risk notes for small-capital intraday trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ycyjy](https://clawhub.ai/user/ycyjy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-tool developers can use this skill to generate daily A-share market momentum reports, candidate watchlists, and position-sizing guidance. Outputs are informational and should be reviewed before any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext credentials may be stored in YAML configuration for data providers, email, or webhook services.

Mitigation: Use environment variables or a local secret manager, and review where configuration files are stored and backed up before adding credentials.

Risk: Scheduled execution can generate or send financial reports without an explicit per-run review.

Mitigation: Check any cron job before enabling the skill and require manual review of generated reports before acting on them.

Risk: Generated financial reports may be persisted locally by default.

Mitigation: Review and manage files saved under ~/.openclaw/workspace/reports, especially on shared or backed-up systems.

Risk: Market reports and win-rate estimates may be incorrect, stale, or misleading.

Mitigation: Treat outputs as informational only, verify data against trusted market sources, and make independent trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ycyjy/skills/marcus-a-stock)
- [Tushare registration](https://tushare.pro/register)
- [JoinQuant](https://www.joinquant.com/)
- [iFinD](https://www.51ifind.com/)
- [ServerChan](http://sc.ftqq.com/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with tables, console text, and optional saved markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated reports under ~/.openclaw/workspace/reports and can use local YAML configuration for data-provider and notification settings.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
