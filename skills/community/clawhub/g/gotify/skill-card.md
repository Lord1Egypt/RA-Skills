## Description: <br>
Send push notifications via Gotify when long-running tasks complete or important events occur. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send Gotify notifications for long-running task completion, status updates, important events, or errors. It can produce shell commands and notification payloads with optional title, priority, and Markdown formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends notification content and an app token to the configured Gotify server. <br>
Mitigation: Use HTTPS, configure a trusted Gotify server, create an app token limited to message creation, and avoid putting secrets or highly sensitive details in notification text. <br>
Risk: A local credentials file stores the Gotify server URL and token. <br>
Mitigation: Restrict credential file permissions and keep the token scoped to the minimum Gotify permissions needed. <br>


## Reference(s): <br>
- [Gotify API docs](https://gotify.net/docs/) <br>
- [ClawHub Gotify release page](https://clawhub.ai/jmagar/gotify) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a Gotify server over HTTPS and return the Gotify message API response.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
