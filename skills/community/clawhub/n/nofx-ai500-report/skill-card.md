## Description:

Generate periodic crypto market intelligence reports from the NOFX AI500 system, including coin-selection monitoring, open interest, institutional flows, K-line technicals, delta, long-short ratios, funding rates, and Telegram or messaging summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinkle-community](https://clawhub.ai/user/tinkle-community)

### License/Terms of Use:

MIT

## Use Case:

Developers, trading-operations teams, and external users can use this skill to set up recurring AI500 crypto market reports, new-coin alerts, and signal summaries from NOFX and public market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background jobs call external market APIs and can send messages to Telegram or another delivery channel.

Mitigation: Install only after approving the schedule, destination channel, and an easy way to disable the cron jobs.

Risk: The release evidence reports unsafe credential handling, including embedded NOFX credentials and use of auth keys in request URLs.

Mitigation: Remove and rotate embedded keys before use, load secrets from protected configuration, and avoid placing keys in prompts or URLs where possible.

Risk: The release evidence reports a monitor.sh path interpolation weakness.

Mitigation: Fix and test the monitor script with a non-sensitive test configuration before enabling recurring execution.

Risk: The optional video and TTS workflow can share report data with additional third-party services.

Mitigation: Use the video-report path only after approving its dependencies, data sharing, and generated media storage.

## Reference(s):

- [NOFX AI500 Report Skill Page](https://clawhub.ai/tinkle-community/skills/nofx-ai500-report)
- [AI500 Report Generator](references/ai500-report.py)
- [Monitor Job](references/monitor-job.md)
- [Report Job](references/report-job.md)
- [Video Report Pipeline](references/video-pipeline.md)
- [NOFX API Base](https://nofxos.ai)
- [Binance Futures K-line API](https://fapi.binance.com/fapi/v1/klines?symbol=XXXUSDT&interval=15m&limit=10)
- [MiniMax TTS API](https://api.minimax.chat/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON cron payloads, shell commands, and formatted report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate recurring market-monitoring jobs, Telegram or messaging alerts, and optional video-report workflow guidance.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
