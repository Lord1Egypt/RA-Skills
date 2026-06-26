## Description: <br>
Connect your AI assistant to GoHighLevel CRM via the official API v2 to manage contacts, conversations, calendars, pipelines, invoices, payments, workflows, and 30+ endpoint groups through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10xcoldleads](https://clawhub.ai/user/10xcoldleads) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, operators, and developers use this skill to let an assistant configure and operate GoHighLevel CRM workflows, contacts, messaging, calendars, pipelines, invoices, payments, and related business records through predefined API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an assistant live authority to change CRM data, send messages, delete records or configuration, enroll workflows, create invoices, record payments, upload external URLs, and publish social posts. <br>
Mitigation: Require human confirmation before mutating CRM data or sending communications, and start with a sub-account Private Integration using only the scopes needed for the intended workflow. <br>
Risk: A GoHighLevel token can expose business CRM data or broaden assistant authority if shared, echoed, stored insecurely, or created at agency scope when sub-account scope is sufficient. <br>
Mitigation: Keep HIGHLEVEL_TOKEN out of chat transcripts and logs, store it as an environment secret, rotate it when access changes, and avoid agency-wide tokens unless multi-location access is required. <br>


## Reference(s): <br>
- [GoHighLevel skill page](https://clawhub.ai/10xcoldleads/highlevel) <br>
- [LaunchMyOpenClaw homepage](https://launchmyopenclaw.com) <br>
- [GoHighLevel API docs](https://marketplace.gohighlevel.com/docs/) <br>
- [GoHighLevel OpenAPI specs](https://github.com/GoHighLevel/highlevel-api-docs) <br>
- [GoHighLevel webhook integration guide](https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide) <br>
- [Contacts reference](references/contacts.md) <br>
- [Conversations reference](references/conversations.md) <br>
- [Calendars reference](references/calendars.md) <br>
- [Opportunities reference](references/opportunities.md) <br>
- [Invoices and payments reference](references/invoices-payments.md) <br>
- [Locations and users reference](references/locations-users.md) <br>
- [Social media reference](references/social-media.md) <br>
- [Forms, surveys, and funnels reference](references/forms-surveys-funnels.md) <br>
- [Advanced API reference](references/advanced.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HIGHLEVEL_TOKEN and HIGHLEVEL_LOCATION_ID environment variables; helper scripts use GoHighLevel API v2 over HTTPS.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
