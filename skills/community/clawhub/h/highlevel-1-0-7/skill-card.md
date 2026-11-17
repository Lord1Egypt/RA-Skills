## Description:

Connect your AI assistant to GoHighLevel CRM via the official API v2 to manage contacts, conversations, calendars, pipelines, invoices, payments, workflows, and more through natural language with setup guidance and pre-built API commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbright4497](https://clawhub.ai/user/mbright4497)

### License/Terms of Use:

MIT-0

## Use Case:

CRM operators, marketers, and developers use this skill to connect an assistant to GoHighLevel for contacts, conversations, calendars, opportunities, invoices, payments, workflows, and related API tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad live CRM actions, including delete, send, billing, social posting, workflow, bulk, and agency-level actions.

Mitigation: Require explicit user confirmation before high-impact operations and review the requested action, target record, and account scope before execution.

Risk: GoHighLevel tokens can expose sensitive customer and business data.

Mitigation: Use a least-privilege sub-account integration, store tokens only in environment variables, treat them like passwords, and rotate them on a regular schedule.

Risk: Agency-wide integrations can affect multiple sub-accounts.

Mitigation: Prefer sub-account integrations for normal use and grant agency-level access only when the task requires multi-location administration.

## Reference(s):

- [Highlevel ClawHub Release](https://clawhub.ai/mbright4497/skills/highlevel-1-0-7)
- [LaunchMyOpenClaw](https://launchmyopenclaw.com)
- [GoHighLevel API Docs](https://marketplace.gohighlevel.com/docs/)
- [GoHighLevel API OpenAPI Specs](https://github.com/GoHighLevel/highlevel-api-docs)
- [GoHighLevel Webhook Integration Guide](https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide)
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

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HIGHLEVEL_TOKEN and HIGHLEVEL_LOCATION_ID for authenticated GoHighLevel requests.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta reports 1.0.7 and SKILL.md frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
