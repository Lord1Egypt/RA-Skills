## Description:

Conversational PolySports trading and OpenClaw automation through structured `/skills/v1` endpoints. Use when user needs to look up PolySports markets, inspect balances or authorization, buy or sell real positions, redeem settled positions, or set up scheduled pregame scans, in-game monitoring, or postgame review workflows while keeping user confirmation in plain language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamcoin1998](https://clawhub.ai/user/dreamcoin1998)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover PolySports sports markets, inspect account state, place or exit real-money positions, redeem settled positions, and configure scheduled pregame, in-game, and postgame automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real-money PolySports trades and persistent automation.

Mitigation: Require explicit order size, plain-language confirmation or delegated authority, preview writes where possible, and set spending limits before enabling scheduled jobs.

Risk: The security review reports unsafe handling of trading credentials in chat and cron-job text.

Mitigation: Use protected secret storage for API keys, avoid pasting live keys into chat or cron payloads, review saved schedules, and rotate any key exposed in a transcript or saved job.

Risk: Automated monitoring can continue after market conditions or positions change.

Mitigation: Review enabled schedules, deliver critical jobs to a monitored channel, report every run outcome, and remove short-lived monitoring jobs after exit or when no longer useful.

## Reference(s):

- [PolySports Skills API](artifact/references/skills-api.md)
- [PolySports Trading Playbook](artifact/references/trading-playbook.md)
- [PolySports Monitoring Rules](artifact/references/monitoring-rules.md)
- [OpenClaw Cron Job Template](artifact/assets/cron/jobs.template.json)
- [Monitor Launcher Prompt Template](artifact/assets/templates/monitor-launcher.prompt.md)
- [PolySports Website](https://polysports.vip)
- [PolySports API Host](https://api.polysports.vip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-language summaries with structured API and automation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-money trade summaries, confirmation prompts, monitoring instructions, cron job configuration, and post-trade review guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
