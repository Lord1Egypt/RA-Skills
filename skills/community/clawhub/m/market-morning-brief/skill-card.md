## Description: <br>
Daily morning and evening intelligence digest for prediction market traders, covering Kalshi portfolio P&L, Polymarket activity, crypto prices, optional cache-based trading signals, and AI-filtered evening news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Prediction market traders use this skill to generate short daily market briefings with portfolio status, public market activity, optional signal caches, and evening news summaries. It is intended for users who can review trading data sources and configure credentials or notification destinations deliberately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs can include sensitive trading positions and P&L and may be sent to a Slack webhook when OPENCLAW_SLACK_WEBHOOK or a configured webhook is present. <br>
Mitigation: Set Slack webhook variables only for destinations that should receive the full brief, and review notification behavior before running with real portfolio data. <br>
Risk: Dry-run behavior for the morning brief does not reliably prevent Slack notification side effects when a webhook is configured. <br>
Mitigation: Unset OPENCLAW_SLACK_WEBHOOK and remove configured webhook URLs when testing, or run in an isolated environment before enabling scheduled use. <br>
Risk: The skill uses trading API credentials and local state files for portfolio, signal, and news history data. <br>
Mitigation: Use least-privileged read-only trading API credentials, protect local state under ~/.openclaw/state, and review stored evening news history. <br>
Risk: The evening scorecard path may import sibling skill code for Kalshalyst scorecard behavior. <br>
Mitigation: Verify the sibling skill path before use or disable that scorecard behavior if importing adjacent skill code is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingmadellc/market-morning-brief) <br>
- [Section documentation](references/sections.md) <br>
- [Integration guide](references/integration.md) <br>
- [Evening briefing pipeline](references/evening-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text briefings with command-line and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Morning and evening scripts can call external APIs, read local cache files, and optionally send the generated brief to Slack when configured.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
