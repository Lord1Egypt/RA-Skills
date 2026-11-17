## Description:

HubSpot CRM API integration with managed OAuth for managing contacts, companies, deals, pipelines, tickets, products, line items, marketing emails, and workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and sales or marketing teams use this skill to work with HubSpot CRM data through ClawLink-managed OAuth. It supports read workflows, CRM updates, marketing operations, workflow management, and guided confirmation for write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires users to trust ClawLink and grant HubSpot OAuth permissions that can include CRM write access.

Mitigation: Review the HubSpot OAuth permissions before connecting and install only when the ClawLink and ClawHub plugin sources are trusted.

Risk: Create, update, archive, delete, batch, and GDPR operations can alter or remove CRM records.

Mitigation: Preview write or destructive operations, confirm the target resource and intended effect with the user, and keep explicit confirmation before execution.

## Reference(s):

- [HubSpot API Documentation](https://developers.hubspot.com/docs/overview)
- [HubSpot CRM Contacts API Reference](https://developers.hubspot.com/docs/api/crm/contacts)
- [HubSpot CRM Deals API Reference](https://developers.hubspot.com/docs/api/crm/deals)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink HubSpot Connection](https://claw-link.dev/dashboard?add=hubspot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline bash commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live HubSpot tool catalog as the source of truth; write and destructive operations require preview and explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
