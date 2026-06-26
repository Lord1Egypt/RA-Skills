## Description: <br>
MailerLite API integration with managed OAuth for managing email subscribers, groups, campaigns, automations, forms, fields, segments, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a MailerLite account through Maton-managed OAuth and perform subscriber, group, campaign, automation, form, segment, field, and webhook operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real MailerLite account-changing actions such as sends, deletes, webhook changes, automation changes, and subscriber changes. <br>
Mitigation: Require explicit user confirmation before any create, update, delete, send, schedule, webhook, automation, or subscriber-change action. <br>
Risk: The skill requires sensitive credentials and proxies access through Maton-managed OAuth. <br>
Mitigation: Keep MATON_API_KEY private and install only when the user trusts Maton to proxy the connected MailerLite account. <br>
Risk: Multiple MailerLite connections can cause requests to affect the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one MailerLite account is connected. <br>


## Reference(s): <br>
- [ClawHub MailerLite skill page](https://clawhub.ai/byungkyu/mailerlite) <br>
- [Related API Gateway skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Maton](https://maton.ai) <br>
- [Maton settings](https://maton.ai/settings) <br>
- [MailerLite API Documentation](https://developers.mailerlite.com/docs/) <br>
- [MailerLite Subscribers API](https://developers.mailerlite.com/docs/subscribers.html) <br>
- [MailerLite Groups API](https://developers.mailerlite.com/docs/groups.html) <br>
- [MailerLite Campaigns API](https://developers.mailerlite.com/docs/campaigns.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid MailerLite OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
