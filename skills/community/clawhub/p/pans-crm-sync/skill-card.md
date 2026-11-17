## Description:

Pans Crm Sync helps agents work with Salesforce and HubSpot customer data workflows, including contact synchronization, pipeline status updates, and customer record queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to run CRM workflows against Salesforce or HubSpot, including syncing recent contacts, updating pipeline stages, and querying customer records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live CRM credentials and customer data.

Mitigation: Review the code before installation, use least-privilege CRM integration credentials, and treat generated outputs as sensitive customer data.

Risk: The security summary flags misleading capability claims and weak safeguards.

Mitigation: Avoid broad or automatic invocation and validate the claimed sync, reporting, and update behavior before production use.

Risk: The security guidance identifies Salesforce query injection as an issue to fix before production use.

Mitigation: Do not use the Salesforce query path with untrusted input until the query construction is remediated and reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with CLI commands and JSON-capable script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CRM credentials from environment variables and can write JSON results when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
