## Description: <br>
Unified Microsoft 365 skill for OpenClaw with modular features for Exchange Online email, SharePoint, OneDrive, Planner, and Microsoft Graph webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felox63](https://clawhub.ai/user/felox63) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IT automation teams use this skill to let an agent work with Microsoft 365 mail, files, SharePoint sites, OneDrive storage, Planner tasks, and webhook-driven workflows through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Microsoft Graph application permissions can expose mailboxes, sites, OneDrive files, and Planner groups beyond the intended workflow. <br>
Mitigation: Use a dedicated Azure app registration with the narrowest practical permissions and restrict access to specific mailboxes, sites, and Planner groups before running the skill. <br>
Risk: The webhook handler can process invoice emails, change mailbox and SharePoint state, and send email-derived details to Telegram. <br>
Mitigation: Run scripts/webhook-handler.js only when that workflow is explicitly approved; disable Telegram settings where external messaging is not allowed. <br>
Risk: Generated environment files contain Microsoft 365 client secrets and webhook secrets. <br>
Mitigation: Protect the .env file as a secret, keep it out of version control, and rotate credentials according to local policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/felox63/m365-unified) <br>
- [Webhook Integration Guide](docs/webhooks.md) <br>
- [Security Audit](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft 365 tenant configuration, Azure app credentials, and feature-specific Microsoft Graph permissions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
