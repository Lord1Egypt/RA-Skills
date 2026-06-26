## Description: <br>
AI dating assistant. Check matching progress, relay deep questions, report results for your human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this agent skill to monitor AILove matching status, relay pending questions to the human, submit the human's verbatim answers, and summarize match results or dating tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive AILove Agent Key for authenticated API access. <br>
Mitigation: Store the key with restrictive local permissions or a secret manager, avoid pasting or logging it unnecessarily, and send it only to the documented AILove API domain. <br>
Risk: Scheduled dating updates may reveal sensitive personal or relationship information in notification channels. <br>
Mitigation: Enable scheduled checks and channel notifications only for private destinations controlled by the user. <br>


## Reference(s): <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove skill document](https://heerweiyi.cc/skill.md) <br>
- [ClawHub skill page](https://clawhub.ai/thesamething/heerweiyi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and concise user-facing status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the AILove matching API, submit human-provided question answers, and provide cron setup guidance.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
