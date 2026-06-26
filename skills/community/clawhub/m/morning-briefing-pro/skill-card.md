## Description: <br>
Generate a daily morning briefing (weather, calendar, news, reminders) using the local `briefing` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddakju](https://clawhub.ai/user/ddakju) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to run a local daily briefing workflow for weather, calendar events, RSS headlines, and due reminders without consuming API tokens for data gathering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface private calendar and reminder information in briefing output. <br>
Mitigation: Grant Calendar and Reminders permissions only when that data should be included, and review briefing output before sharing it. <br>
Risk: Automated cron or HEARTBEAT scheduling can relay private briefing output without a fresh prompt each time. <br>
Mitigation: Enable scheduled runs only after confirming the recipient, timing, and contents are appropriate for automatic delivery. <br>
Risk: The skill depends on an external npm CLI package and local `briefing` binary. <br>
Mitigation: Install only from a trusted package source and keep the local CLI updated before using the skill. <br>


## Reference(s): <br>
- [Morning Briefing ClawHub release](https://clawhub.ai/ddakju/morning-briefing-pro) <br>
- [ddakju publisher profile](https://clawhub.ai/user/ddakju) <br>
- [@openclaw-tools/morning-briefing npm package](https://www.npmjs.com/package/@openclaw-tools/morning-briefing) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the CLI can emit readable text, compact text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS only; requires the local `briefing` binary and optional Calendar/Reminders permissions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
