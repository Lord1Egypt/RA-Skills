## Description: <br>
Matching pipeline dashboard—phase, countdown, pending Q&A, and outcome summaries. Same official AILove /agent/matching API as loveq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to check AILove matching status, relay pending questions, submit the human's verbatim answers, and configure scheduled morning and evening status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AILove Agent Key to access matching data. <br>
Mitigation: Install only when the user trusts AILove/heerweiyi.cc, keep the key in an environment variable or secret store, and revoke it if exposed. <br>
Risk: Scheduled notifications can send matching updates to the wrong channel if misconfigured. <br>
Mitigation: Verify the notification channel target before enabling cron jobs. <br>
Risk: The skill can submit answers to pending matching questions. <br>
Mitigation: Submit only the human's verbatim answer and do not fabricate responses or request profile/contact details unavailable through the documented endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thesamething/match) <br>
- [AILove Homepage](https://heerweiyi.cc) <br>
- [AILove Agent API Base](https://heerweiyi.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AILOVE_API_KEY and may use scheduled notification channel targets.] <br>

## Skill Version(s): <br>
1.4.2 (source: frontmatter, claw.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
