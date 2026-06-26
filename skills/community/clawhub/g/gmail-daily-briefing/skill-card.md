## Description: <br>
Fetch Gmail emails from the last 24h, rank by importance, summarize into bullet points, and auto-create Google Calendar events for detected meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russidan-nadee](https://clawhub.ai/user/russidan-nadee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to review recent Gmail messages, receive concise bullet summaries, and create calendar events for detected meetings or interviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google OAuth scopes for Gmail read access and Calendar event creation. <br>
Mitigation: Use a low-risk Google account when possible and revoke the OAuth grant when the skill is no longer needed. <br>
Risk: The skill stores persistent OAuth credentials in token.json. <br>
Mitigation: Protect token.json, avoid sharing the workspace, and delete the token when access is no longer required. <br>
Risk: Fetched email bodies may be printed in full during processing. <br>
Mitigation: Run the skill only in trusted agent environments and avoid using it on accounts with highly sensitive mail unless that exposure is acceptable. <br>
Risk: Calendar events may be created from detected meeting details without strong confirmation. <br>
Mitigation: Ask the agent to show proposed calendar events before creating them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/russidan-nadee/gmail-daily-briefing) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [OpenClaw](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown bullet summaries with inline command-driven actions and calendar creation status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print full fetched email contents during processing and may create Google Calendar events when meeting details are detected.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
