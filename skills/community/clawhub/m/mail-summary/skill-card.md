## Description: <br>
Fetch Gmail emails from the last 24h, rank by importance, summarize into bullet points, and auto-create Google Calendar events for detected meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russidan-nadee](https://clawhub.ai/user/russidan-nadee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who want an agent to review recent Gmail messages use this skill to summarize important email content and create Google Calendar events for detected meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ongoing Gmail read access and Google Calendar event-write access. <br>
Mitigation: Install only when that account access is acceptable, keep OAuth credential files out of shared logs and repositories, and know how to revoke the Google OAuth grant and delete token.json. <br>
Risk: Detected meetings can lead to calendar events being created. <br>
Mitigation: Require the agent to show proposed calendar events for approval before creating them. <br>
Risk: Automatic background token refresh can preserve access longer than intended. <br>
Mitigation: Avoid or disable automatic background refresh unless continuous access is explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/russidan-nadee/mail-summary) <br>
- [Publisher profile](https://clawhub.ai/user/russidan-nadee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style email summaries with setup guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Google Calendar events after the agent detects meetings in fetched emails.] <br>

## Skill Version(s): <br>
1.1.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
