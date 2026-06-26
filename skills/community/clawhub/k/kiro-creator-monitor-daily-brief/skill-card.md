## Description: <br>
Monitor creator topics across X, RSS, GitHub, and Reddit; deduplicate and score results; produce a daily top-5 brief plus one publish-ready X/LinkedIn draft; optional scheduled delivery to Telegram, Slack, or email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vmining](https://clawhub.ai/user/Vmining) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, operators, and developer teams use this skill to monitor configured AI, Web3, GitHub, RSS, Reddit, and X sources, then generate a concise daily brief and social draft for follow-up publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs can leave the local environment when Telegram, Slack, or email delivery is enabled. <br>
Mitigation: Enable delivery only for approved destinations, verify recipient and webhook settings before scheduling, and keep sensitive monitoring topics local. <br>
Risk: The skill uses API tokens and delivery credentials for X, Telegram, Slack, and SMTP. <br>
Mitigation: Use dedicated low-privilege credentials, store them in environment variables, and rotate them if a destination or workspace changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vmining/kiro-creator-monitor-daily-brief) <br>
- [Kiro AI homepage](https://kiroai.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily brief, JSON summary, setup commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes latest.md and latest.json, and can optionally deliver the Markdown brief to Telegram, Slack, or email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
