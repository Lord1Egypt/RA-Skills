## Description: <br>
Email for AI agents. Create mailboxes, send and receive emails via API. No browser, no OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishavmukherji](https://clawhub.ai/user/rishavmukherji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create agent-accessible mailboxes, send email, check inboxes, search messages, and register webhooks through the Neynar Inbox REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles email content and mailbox metadata through the Neynar Inbox service. <br>
Mitigation: Install only if the user trusts Neynar Inbox with the email data handled by the agent. <br>
Risk: Generated mailbox API keys are returned once and cannot be recovered. <br>
Mitigation: Store generated API keys immediately in a secret store and rotate keys if they may have been exposed. <br>
Risk: Sending email, deleting email, or deleting mailboxes can create external effects or data loss. <br>
Mitigation: Require explicit confirmation before sending or deleting email or mailboxes. <br>
Risk: Webhook registration and polling can expose or route email events to unintended destinations. <br>
Mitigation: Only register webhook URLs and polling schedules that the user intentionally controls, and verify webhook signatures. <br>


## Reference(s): <br>
- [Neynar Inbox homepage](https://email.neynar.ai) <br>
- [ClawHub skill page](https://clawhub.ai/rishavmukherji/neynar-inbox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes REST API endpoint, authentication, webhook, error code, and mailbox limit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
