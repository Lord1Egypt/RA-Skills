## Description: <br>
CT Monitor helps OpenClaw users monitor crypto KOL tweets, real-time news, RSS feeds, market prices, smart-money signals, and on-chain/social hype data to generate crypto intelligence reports and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tizerluo](https://clawhub.ai/user/tizerluo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and crypto market researchers use this skill to query CT Monitor APIs, combine KOL tweets, news, price, and smart-money data, and synthesize Markdown market briefings, alerts, token research, and scheduled reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends CT Monitor API keys and crypto research queries to the CT Monitor service. <br>
Mitigation: Install only if the user trusts CT Monitor, store the key in CT_MONITOR_API_KEY, and rotate or remove the key when access is no longer needed. <br>
Risk: Some documented CT Monitor endpoints incur paid API-call charges. <br>
Mitigation: Review endpoint costs before running workflows, especially scheduled or repeated reports. <br>
Risk: The skill can propose watchlist add or remove actions. <br>
Mitigation: Confirm watchlist changes before executing subscription POST or DELETE requests. <br>
Risk: Scheduled Telegram jobs can repeatedly send reports outside OpenClaw. <br>
Mitigation: Create cron or Telegram jobs only for reports the user intentionally wants delivered on a recurring schedule, and periodically review active jobs. <br>


## Reference(s): <br>
- [CT Monitor API Docs](https://api.ctmon.xyz/api/docs) <br>
- [Project Homepage](https://github.com/tizerluo/ct-monitor-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/tizerluo/openclaw-twitter-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CT_MONITOR_API_KEY and may generate scheduled OpenClaw cron or Telegram delivery commands when requested.] <br>

## Skill Version(s): <br>
3.3.18 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
