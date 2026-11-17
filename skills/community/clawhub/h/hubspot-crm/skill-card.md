## Description:

Provides HubSpot CRM command guidance for USC SYNERGY, including contact and deal search, creation, updates, associations, pipeline reporting, and contact archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibbou](https://clawhub.ai/user/mibbou)

### License/Terms of Use:


## Use Case:

CRM operators and agents use this skill to manage USC SYNERGY HubSpot contacts, deals, notes, tasks, associations, and daily pipeline checks through documented cURL commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create, update, associate, or archive live HubSpot CRM records.

Mitigation: Require human confirmation for write and archive payloads before execution.

Risk: A broad HubSpot access token could expose or modify more CRM data than the workflow needs.

Mitigation: Use a least-privilege HUBSPOT_ACCESS_TOKEN scoped only to the required CRM operations.

Risk: Placeholder n8n webhooks could send CRM data to workflows whose ownership, authentication, or data handling has not been verified.

Mitigation: Enable webhook workflows only after confirming their owner, authentication controls, and data-processing behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibbou/skills/hubspot-crm)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with cURL command examples and CRM workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require HUBSPOT_ACCESS_TOKEN and may read, create, update, associate, or archive HubSpot CRM records.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
