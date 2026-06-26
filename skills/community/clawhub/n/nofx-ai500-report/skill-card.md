## Description: <br>
Generates periodic crypto market intelligence reports from the NOFX AI500 system by monitoring coin selections and analyzing open interest, institutional fund flows, K-line technicals, delta, long-short ratios, and funding rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinkle-community](https://clawhub.ai/user/tinkle-community) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure recurring NOFX AI500 crypto market reports, new-coin alerts, and delivery to Telegram or another messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports a real-looking embedded NOFX API key and credential use in URLs or cron messages. <br>
Mitigation: Replace the bundled default key before use, rotate it if it was real, and pass secrets through environment variables or a secret store instead of hard-coded values. <br>
Risk: The skill configures recurring jobs that send market data and credentials through external NOFX, Binance, Telegram, and optional MiniMax TTS services. <br>
Mitigation: Review outbound destinations and cron payloads before enabling them, confirm the Telegram target, and document how to remove scheduled jobs and local known-coin state. <br>
Risk: Automated crypto market reports and trading suggestions can be stale, incomplete, or misleading. <br>
Mitigation: Require human review before acting on generated reports and avoid treating the output as financial advice or the sole basis for trading decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tinkle-community/nofx-ai500-report) <br>
- [AI500 report generator](references/ai500-report.py) <br>
- [Monitor job template](references/monitor-job.md) <br>
- [Report job template](references/report-job.md) <br>
- [Video report pipeline](references/video-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON cron payloads, shell command output, and Python or Bash code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create recurring cron jobs, outbound API calls, Telegram messages, local known-coin state, and optional video or TTS assets when configured.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
