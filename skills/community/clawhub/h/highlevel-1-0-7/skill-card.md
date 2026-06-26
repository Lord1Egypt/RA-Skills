## Description: <br>
Connects an AI assistant to GoHighLevel CRM through the official API v2 for contacts, conversations, calendars, pipelines, invoices, payments, workflows, and related endpoint groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbright4497](https://clawhub.ai/user/mbright4497) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and CRM administrators use this skill to configure a GoHighLevel private integration and let an assistant produce setup guidance, safe helper-script commands, and API-oriented CRM actions. Typical tasks include searching and updating contacts, sending messages, booking appointments, reviewing opportunities, creating invoices, managing workflows, and troubleshooting API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an assistant broad live CRM authority. <br>
Mitigation: Use a sub-account token with the smallest scopes needed and start with read-only scopes where possible. <br>
Risk: Write actions such as deletes, messages, appointments, invoices, workflow changes, and social posts can affect customers or business records. <br>
Mitigation: Manually confirm those actions before allowing the assistant to execute them. <br>
Risk: Bearer tokens can expose CRM access if printed, shared, or entered in an unsafe environment. <br>
Mitigation: Do not print or share the token, and run setup only in a private terminal. <br>
Risk: Agency-level, financial, or broad write scopes increase impact if the assistant makes a mistake. <br>
Mitigation: Avoid agency-level or financial/write scopes unless the use case clearly requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbright4497/highlevel-1-0-7) <br>
- [LaunchMyOpenClaw homepage](https://launchmyopenclaw.com) <br>
- [GoHighLevel API docs](https://marketplace.gohighlevel.com/docs/) <br>
- [GoHighLevel OpenAPI specs](https://github.com/GoHighLevel/highlevel-api-docs) <br>
- [GoHighLevel webhook integration guide](https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide) <br>
- [Contacts API reference](references/contacts.md) <br>
- [Conversations API reference](references/conversations.md) <br>
- [Calendars API reference](references/calendars.md) <br>
- [Opportunities API reference](references/opportunities.md) <br>
- [Invoices and payments API reference](references/invoices-payments.md) <br>
- [Locations and users API reference](references/locations-users.md) <br>
- [Social media API reference](references/social-media.md) <br>
- [Forms, surveys, and funnels API reference](references/forms-surveys-funnels.md) <br>
- [Advanced API reference](references/advanced.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python helper-script invocations, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HIGHLEVEL_TOKEN and HIGHLEVEL_LOCATION_ID environment variables and network access to services.leadconnectorhq.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0 and artifact _meta.json reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
