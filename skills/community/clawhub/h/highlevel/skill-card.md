## Description:

Connects an AI assistant to GoHighLevel API v2 so it can manage CRM contacts, conversations, calendars, pipelines, invoices, payments, workflows, and related endpoint groups through guided commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10xcoldleads](https://clawhub.ai/user/10xcoldleads)

### License/Terms of Use:


## Use Case:

Developers, CRM operators, and automation teams use this skill to connect an assistant to a GoHighLevel sub-account and run guided CRM actions such as contact search, messaging, booking, pipeline updates, invoice work, workflow enrollment, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live customer, billing, messaging, workflow, social posting, and account data with a bearer token.

Mitigation: Use a least-privilege sub-account token and require explicit review before commands that send, delete, invoice, record payment, enroll workflows, post socially, or change account settings.

Risk: An agency-wide token could expose multiple sub-accounts to unintended actions.

Mitigation: Start with a sub-account integration and grant only the scopes needed for the intended workflow.

Risk: Sensitive tokens could be exposed if HTTP redirects leave the intended API origin.

Mitigation: Patch or wrap the scripts to block cross-origin redirects before using production credentials.

## Reference(s):

- [GoHighLevel skill page](https://clawhub.ai/10xcoldleads/skills/highlevel)
- [LaunchMyOpenClaw](https://launchmyopenclaw.com)
- [GoHighLevel API documentation](https://marketplace.gohighlevel.com/docs/)
- [GoHighLevel OpenAPI specs](https://github.com/GoHighLevel/highlevel-api-docs)
- [GoHighLevel webhook integration guide](https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide)
- [Contacts API Reference](references/contacts.md)
- [Conversations & Messaging API Reference](references/conversations.md)
- [Calendars & Appointments API Reference](references/calendars.md)
- [Opportunities & Pipelines API Reference](references/opportunities.md)
- [Invoices, Payments & Products API Reference](references/invoices-payments.md)
- [Locations & Users API Reference](references/locations-users.md)
- [Social Media Planner API Reference](references/social-media.md)
- [Forms, Surveys & Funnels API Reference](references/forms-surveys-funnels.md)
- [Advanced API Reference](references/advanced.md)
- [Troubleshooting Reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HIGHLEVEL_TOKEN and HIGHLEVEL_LOCATION_ID; live API effects depend on the bearer token scopes.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
