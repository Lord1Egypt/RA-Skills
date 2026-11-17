## Description:

P-API - WhatsApp API helps agents automate WhatsApp messaging, interactive content, instance and group management, product catalogs, integrations, and webhooks through the P-API service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and call P-API endpoints for WhatsApp automation, including sending media messages, creating instances, managing groups and catalogs, and connecting webhooks or integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful messaging and account-management actions can send messages, remove instances, alter groups, update catalogs, or connect outbound event streams.

Mitigation: Use least-privilege, instance-scoped API keys and require explicit confirmation for recipients, group changes, destructive deletes, catalog changes, and webhook or WebSocket destinations.

Risk: Weak credential-handling guidance can expose API keys or message/account data.

Mitigation: Avoid storing real keys in repositories or agent-readable Markdown, use trusted HTTPS/WSS endpoints, and enable only the event types needed for the deployment.

## Reference(s):

- [P-API official website](https://papi.api.br)
- [Mundo Automatik](https://mundoautomatik.com/)
- [Interactive messages reference](references/interactive.md)
- [Groups reference](references/groups.md)
- [Product catalog reference](references/catalog.md)
- [Integrations reference](references/integrations.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint paths, request headers, request bodies, and operational cautions for WhatsApp automation.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
