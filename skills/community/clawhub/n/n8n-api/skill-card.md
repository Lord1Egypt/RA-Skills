## Description:

Operate n8n via its public REST API from OpenClaw for workflow management, executions, and automation tasks across self-hosted n8n and n8n Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to manage and troubleshoot n8n workflows, executions, credentials, projects, tags, variables, data tables, users, audits, source-control pulls, and webhooks through the public REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for live n8n administrative actions, including workflow activation, deactivation, retries, credential operations, role changes, and delete requests.

Mitigation: Use a least-privileged n8n API key, confirm the target instance and resource identifiers before any mutating action, and prefer a test workflow or test instance for experiments.

Risk: Webhook examples can trigger real production or test workflows.

Mitigation: Confirm whether the URL is a production webhook or test webhook before sending payloads, and use test webhooks for validation whenever possible.

## Reference(s):

- [n8n REST API Endpoint Reference](artifact/assets/n8n-api-endpoints.md)
- [ClawHub Skill Page](https://clawhub.ai/codedao12/skills/n8n-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses N8N_API_BASE_URL and N8N_API_KEY environment variables for examples.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
