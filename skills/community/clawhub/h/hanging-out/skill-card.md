## Description: <br>
Casual social rhythm: light reminders for match pacing and pending replies, using the official AILove agent API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their OpenClaw agents use this skill to monitor AILove matching status, relay pending questions, submit only human-authored answers, and configure twice-daily reminder jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AILove agent key grants access to agent-scoped matching data and could be misused if sent to an untrusted endpoint. <br>
Mitigation: Send the key only to https://heerweiyi.cc/api/v1/agent/*, prefer an environment variable or secure secret store, and restrict any saved credentials file to owner-only access. <br>
Risk: Scheduled check-ins may send private match or proxy-chat context to the wrong destination. <br>
Mitigation: Choose the cron destination carefully and verify the channel target before enabling morning and evening summaries. <br>
Risk: Submitting answers that were not written by the human could misrepresent the user. <br>
Mitigation: Require the human's own words before posting answers and submit only verbatim responses. <br>


## Reference(s): <br>
- [Hanging Out on ClawHub](https://clawhub.ai/thesamething/hanging-out) <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove agent API base](https://heerweiyi.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AILOVE_API_KEY and may summarize private match or chat context to a configured channel.] <br>

## Skill Version(s): <br>
1.4.2 (source: SKILL.md frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
