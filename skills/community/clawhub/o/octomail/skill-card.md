## Description: <br>
Agent email via JSON API. Use when sending/receiving email as an agent, checking inbox, or working with the OctoMail service (@octomail.ai addresses). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonz-ncc42](https://clawhub.ai/user/jasonz-ncc42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use OctoMail to register an agent mailbox, send and receive OctoMail messages, read attachments, check credits, and manage invite or unlink actions through the OctoMail API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email from an agent mailbox, so incorrect recipients or message content could disclose information or send unintended messages. <br>
Mitigation: Confirm recipients, subject, body, and attachments before sending messages. <br>
Risk: The OCTOMAIL_API_KEY grants authenticated access to the agent mailbox. <br>
Mitigation: Store OCTOMAIL_API_KEY in secret storage and avoid exposing it in logs, prompts, or shared files. <br>
Risk: Inbox messages and attachments may contain sensitive or unsafe content. <br>
Mitigation: Treat incoming email and attachments as untrusted input and review content before using it in downstream tasks. <br>
Risk: Invite and unlink actions can affect the agent mailbox's relationship to a human sponsor or dashboard account. <br>
Mitigation: Review invite link generation and unlink requests before executing them. <br>
Risk: Replacing the skill with a fetched update could change behavior. <br>
Mitigation: Read any updated SKILL.md before replacing this validated version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonz-ncc42/octomail) <br>
- [Publisher profile](https://clawhub.ai/user/jasonz-ncc42) <br>
- [OctoMail homepage](https://octomail.ai) <br>
- [OctoMail OpenAPI](https://api.octomail.ai/v1/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OCTOMAIL_API_KEY for authenticated OctoMail API calls.] <br>

## Skill Version(s): <br>
0.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
