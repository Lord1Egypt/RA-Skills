## Description:

Full HubSpot CRM automation — contacts, deals, companies, activities, and pipeline reports via the HubSpot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to run command-line HubSpot CRM workflows for contacts, deals, companies, activities, and pipeline reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, modify, and delete live HubSpot CRM records.

Mitigation: Use a least-privilege HubSpot private-app token, remove unused scopes, test against non-production data first, and manually confirm update or delete commands before running them.

Risk: The required HubSpot token grants broad CRM authority if over-scoped or exposed.

Mitigation: Store HUBSPOT_API_KEY outside shared files and rotate the token if it may have been disclosed.

## Reference(s):

- [HubSpot API](https://api.hubapi.com)
- [ClawHub Skill Page](https://clawhub.ai/fr3kstyle/skills/hubspot-crm-skill)
- [Publisher Profile](https://clawhub.ai/user/fr3kstyle)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HubSpot private-app bearer token supplied through HUBSPOT_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
