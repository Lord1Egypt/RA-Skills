## Description:

Pipeworx Airtable lets an agent use an Airtable MCP endpoint to list bases, inspect schemas, fetch or filter records, retrieve record details, and create records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to connect an agent to Airtable data, read base structure and records, and create new records through the configured MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Airtable read and write access through an under-documented third-party gateway.

Mitigation: Grant access only to specific Airtable bases and permissions needed for the workflow, prefer read-only access unless record creation is required, and confirm who operates the gateway and how credentials and Airtable data are handled.

Risk: Record creation can modify Airtable data if the connected credentials have write permission.

Mitigation: Use least-privilege Airtable credentials, review requested operations before enabling write access, and revoke access if operator or data-handling details cannot be confirmed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/brucegutman/skills/pipeworx-airtable)
- [Publisher Profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include Airtable base, schema, record, and creation-result details returned by the MCP endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
