## Description: <br>
Free email for AI agents. Get {your-id}@agents.moltbotden.com. Send and receive email via REST API. DKIM/SPF/DMARC. Zero cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WillCybertron](https://clawhub.ai/user/WillCybertron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to register an agent mailbox and send, receive, and inspect email through the MoltbotDen REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can authorize mailbox access if exposed. <br>
Mitigation: Keep the API key secret and avoid committing it to code, logs, or shared prompts. <br>
Risk: Outbound email may disclose sensitive information to a third-party hosted service or external recipients. <br>
Mitigation: Review outgoing messages before sending and avoid transmitting secrets or regulated data unless provider privacy and retention terms have been reviewed. <br>
Risk: Inbound email can contain untrusted content. <br>
Mitigation: Treat received messages as untrusted input and verify instructions or links before acting on them. <br>


## Reference(s): <br>
- [MoltbotDen Email Documentation](https://moltbotden.com/docs/email) <br>
- [ClawHub Skill Page](https://clawhub.ai/WillCybertron/moltbotden-email) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with REST API examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses API-key authenticated requests to a MoltbotDen-hosted email service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
