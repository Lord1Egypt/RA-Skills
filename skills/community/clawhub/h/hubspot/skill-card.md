## Description:

HubSpot CRM and CMS API integration for contacts, companies, deals, owners, and content management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwall1](https://clawhub.ai/user/kwall1)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate HubSpot REST API commands for CRM and CMS workflows, including contacts, companies, deals, owners, associations, properties, pages, domains, and files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can read or change HubSpot CRM and CMS data using a private app token.

Mitigation: Use a minimally scoped private app token, keep it out of files and shared logs, and review commands before execution.

Risk: POST and PATCH examples can create or modify CRM records in a production HubSpot portal.

Mitigation: Prefer a test portal for examples and require explicit approval before running record-changing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kwall1/skills/hubspot)
- [HubSpot Skill Homepage](https://github.com/kwall1/hubspot-skill)
- [HubSpot API Base](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with inline bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq examples with HUBSPOT_ACCESS_TOKEN for authenticated HubSpot API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
