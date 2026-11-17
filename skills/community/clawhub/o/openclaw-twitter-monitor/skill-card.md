## Description:

CT Monitor helps agents monitor crypto KOL tweets, real-time news, RSS feeds, prices, Binance Web3 signals, and on-chain context to produce crypto intelligence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tizerluo](https://clawhub.ai/user/tizerluo)

### License/Terms of Use:


## Use Case:

External users and crypto analysts use this skill to query CT Monitor APIs, correlate KOL activity, news, token prices, alpha signals, and smart-money data, and receive concise market briefings, due-diligence summaries, security alerts, and scheduled monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes authenticated CT Monitor API calls that may consume a paid API balance.

Mitigation: Install only if the user trusts CT Monitor with the API key and billing account; keep CT_MONITOR_API_KEY scoped to this service and review cost-bearing prompts before running them.

Risk: The skill can propose recurring OpenClaw cron jobs that repeatedly call external services and deliver reports.

Mitigation: Review each cron schedule, destination, and prompt before enabling it, and periodically audit active jobs.

Risk: Market reports, links, token signals, and investment suggestions are derived from external crypto data that may be inaccurate, manipulated, stale, or incomplete.

Mitigation: Treat outputs as untrusted market intelligence, require source-backed review before acting, and do not rely on the skill as financial advice.

## Reference(s):

- [Openclaw Twitter Monitor on ClawHub](https://clawhub.ai/tizerluo/skills/openclaw-twitter-monitor)
- [Publisher Profile](https://clawhub.ai/user/tizerluo)
- [CT Monitor Skill Homepage](https://github.com/tizerluo/ct-monitor-skill)
- [CT Monitor API Documentation](https://api.ctmon.xyz/api/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated CT Monitor API calls and may propose scheduled OpenClaw cron jobs for recurring reports.]

## Skill Version(s):

3.3.18 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
