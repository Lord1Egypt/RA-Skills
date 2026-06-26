## Description: <br>
AgentMail Email helps agents create and manage dedicated AgentMail inboxes, send and receive email programmatically, and handle email workflows through webhooks and real-time events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidsteelerose](https://clawhub.ai/user/davidsteelerose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents email identities, send status updates or documents, poll inboxes, and connect incoming email to webhook-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents with AgentMail access can expose private communications, recipients, attachments, or API credentials if email actions are not reviewed. <br>
Mitigation: Store AGENTMAIL_API_KEY as a protected secret, confirm recipients and attachments before sending, and redact sensitive email content before forwarding it into shared systems. <br>
Risk: Incoming email and webhook payloads can carry untrusted instructions that may prompt-inject an agent workflow or trigger unintended automation. <br>
Mitigation: Verify webhook signatures, scope webhooks to trusted endpoints, allowlist trusted senders before triggering agent actions, and route untrusted messages to review. <br>


## Reference(s): <br>
- [AgentMail API Reference](references/API.md) <br>
- [AgentMail Webhooks Guide](references/WEBHOOKS.md) <br>
- [AgentMail Usage Examples](references/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use AgentMail API calls through bundled Python helper scripts when AGENTMAIL_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
