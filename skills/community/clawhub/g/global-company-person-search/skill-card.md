## Description:

Search global corporate personnel by name, company, industry, and profile URL, and help enrich contact data for recruiting, sales, and B2B lead-generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, sales teams, and B2B lead-generation specialists use this skill to search global corporate personnel records, source candidates, identify cross-border contacts, and enrich contact data. It supports targeted searches by person, company, industry, country, profile URL, and contact-availability filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an UpKuaJing API key for paid people-search requests.

Mitigation: Confirm fee-incurring searches before execution and store the API key with restricted local permissions.

Risk: Search results can include retained contact and personnel data.

Mitigation: Limit searches to necessary records, protect saved task data, and delete retained result files when they are no longer needed.

Risk: Top-up and payment-order flows can affect account balance.

Mitigation: Require explicit user confirmation before creating top-up orders or continuing paid operations.

Risk: The skill performs version checks against the UpKuaJing API service.

Mitigation: Review outbound network behavior before installation in restricted environments.

## Reference(s):

- [Global Company Person List API](references/global-company-person-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-person-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results written to task files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are returned as person records and may be saved as task data for continuation.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
