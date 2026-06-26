## Description: <br>
Monitors a user's LinkedIn inbox, alerts on new conversations, and drafts or sends replies according to configured autonomy levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanbaker24](https://clawhub.ai/user/dylanbaker24) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals and teams use this skill to monitor LinkedIn inbox activity, receive alerts in chat channels, and prepare replies in the user's communication style. It supports supervised approval by default and can be configured for higher autonomy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill monitors and forwards private LinkedIn inbox content to a configured alert channel. <br>
Mitigation: Use a private alert channel, limit channel membership, and review the configured destination before enabling scheduled monitoring. <br>
Risk: The skill may store LinkedIn session cookies or credentials locally for account access. <br>
Mitigation: Protect the local credentials file, prefer environment-based secrets where practical, and remove ~/.clawdbot/linkedin-monitor data when the skill is no longer needed. <br>
Risk: Higher autonomy levels can send messages from the user's LinkedIn account automatically. <br>
Mitigation: Keep autonomy at Level 0 or 1 unless outbound-message behavior has been reviewed and daily limits, escalation keywords, and approval workflows are configured. <br>


## Reference(s): <br>
- [LinkedIn Monitor README](README.md) <br>
- [LinkedIn Monitor Setup Guide](docs/SETUP.md) <br>
- [LinkedIn Monitor Troubleshooting](docs/TROUBLESHOOT.md) <br>
- [LinkedIn Monitor Cron Payload](CRON-PAYLOAD.md) <br>
- [Clawdbot project](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state, logs, drafts, and configuration under ~/.clawdbot/linkedin-monitor when used.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
