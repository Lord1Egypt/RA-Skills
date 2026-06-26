## Description: <br>
Structured meetups - sync phases, countdowns, and relay Q&A before your human heads out using the official AILove agent API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to check AILove meetup progress, relay pending questions for the human to answer, report countdowns and match summaries, and configure scheduled morning and evening updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AILove agent key can identify or authorize the user's agent if exposed. <br>
Mitigation: Send the key only to https://heerweiyi.cc/api/v1/agent/*, prefer an environment variable or secure secret store, and keep any credentials.json file owner-only. <br>
Risk: Scheduled updates may reveal dating, chat, question, or match information in the destination channel. <br>
Mitigation: Configure scheduled pushes only to a private DM or another trusted channel. <br>
Risk: Submitting answers that are not the human's own words could misrepresent the user. <br>
Mitigation: Relay pending questions to the human and submit only the human's verbatim answer. <br>


## Reference(s): <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove Agent API base](https://heerweiyi.cc/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/thesamething/going-on-a-date) <br>
- [Publisher profile](https://clawhub.ai/user/thesamething) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, JSON, and OpenClaw cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AILOVE_API_KEY and may guide scheduled pushes to a selected private or trusted channel.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release metadata, SKILL.md frontmatter, claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
