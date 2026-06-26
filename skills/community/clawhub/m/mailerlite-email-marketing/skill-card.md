## Description: <br>
Manage MailerLite email marketing campaigns, automations, subscribers, and e-commerce stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage MailerLite email marketing work through ClawLink, including campaigns, automations, subscribers, groups, segments, e-commerce records, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access and sensitive account credentials through ClawLink. <br>
Mitigation: Install only when MailerLite account access is expected, complete connection through the ClawLink dashboard, and review account or credential prompts before use. <br>
Risk: Write operations can alter campaigns, subscribers, automations, groups, segments, stores, products, orders, carts, and webhooks. <br>
Mitigation: Use tool descriptions and previews before write actions, then execute only after explicit user confirmation of the target resource and intended effect. <br>
Risk: Some destructive actions, including subscriber deletion and GDPR forget operations, are permanent or irreversible after processing. <br>
Mitigation: Confirm destructive requests separately and verify identifiers with read operations before invoking delete or forget tools. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/mailerlite-email-marketing) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>
- [MailerLite API Documentation](https://developers.mailerlite.com/) <br>
- [MailerLite Integrations](https://www.mailerlite.com/integrations) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for ClawLink tool discovery, previews, confirmations, and MailerLite API actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
