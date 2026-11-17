## Description:

Complete Indeed job postings toolkit via RolesAPI.com. Search Indeed job postings by keyword and location, fetch full role details, look up salary for a job posting, and get descriptions, company info, and benefits across 60+ country editions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Indeed listings, inspect specific postings, retrieve salary, company, description, and benefits data, and check RolesAPI account usage when a user explicitly requests job-posting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls send search terms, locations, job keys, pasted Indeed URLs, or account usage requests to RolesAPI.

Mitigation: Use the skill only for explicit job-data requests and avoid sending sensitive personal information in search terms or pasted URLs.

Risk: Most lookup scripts consume RolesAPI credits and can return large records.

Mitigation: Confirm ambiguous user intent before running scripts and prefer narrower endpoints, such as salary, company, benefits, or description, when full posting details are unnecessary.

Risk: Account and usage checks can display plan, rate limit, credit balance, or recent usage records.

Mitigation: Run account and usage scripts only when the user asks for account status or usage information.

## Reference(s):

- [RolesAPI homepage](https://rolesapi.com)
- [RolesAPI OpenAPI specification](https://rolesapi.com/openapi.json)
- [RolesAPI roles API documentation](https://rolesapi.com/api/roles/)
- [RolesAPI listings API documentation](https://rolesapi.com/api/listings/)
- [RolesAPI search API documentation](https://rolesapi.com/api/search/)
- [RolesAPI hosted MCP server](https://api.rolesapi.com/mcp)
- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/indeed-full)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and pretty-printed JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ROLESAPI_KEY; lookup calls may consume RolesAPI credits and return large job-posting records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
