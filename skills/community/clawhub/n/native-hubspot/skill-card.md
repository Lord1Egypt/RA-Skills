## Description:

Query and manage HubSpot CRM data via the HubSpot API, including contacts, companies, deals, tickets, pipelines, owners, record creation, record updates, and associations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and manage HubSpot CRM records from an agent workflow. It supports CRM lookup, creation, update, association, pipeline, and owner tasks using a HubSpot private app token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly create, update, and associate live HubSpot CRM records.

Mitigation: Review target records and intended changes before using create, update, or associate commands, especially in production.

Risk: The skill depends on a HubSpot private app token that may have broad CRM access.

Mitigation: Use a dedicated private app with the narrowest scopes possible and protect HUBSPOT_TOKEN as a secret.

Risk: The helper does not provide a built-in confirmation or dry-run safeguard.

Mitigation: Run read-only list, search, get, pipeline, or owner commands first to verify IDs and data before write operations.

## Reference(s):

- [Native HubSpot on ClawHub](https://clawhub.ai/codeninja23/skills/native-hubspot)
- [Publisher profile](https://clawhub.ai/user/codeninja23)
- [HubSpot CRM API](https://api.hubapi.com/crm/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON or table output from the HubSpot API helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and HUBSPOT_TOKEN; command output depends on live HubSpot CRM data and requested object type.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
