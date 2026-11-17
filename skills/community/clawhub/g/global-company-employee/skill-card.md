## Description:

Retrieves employee records for a specified global company ID through UpKuaJing's global company database, including person identifiers and job titles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting, sales, and B2B lead generation teams use this skill to look up employees associated with a known company ID and support contact enrichment, talent mapping, and decision-maker targeting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reads an UpKuaJing API key for authenticated requests.

Mitigation: Use a scoped API key where possible, avoid sharing or printing it, and remove it from local configuration when access is no longer needed.

Risk: Employee lookup and account top-up operations can incur fees.

Mitigation: Confirm pricing and obtain explicit approval before running any fee-incurring query or payment-related action.

Risk: Diagnostic error reports may include request context or response details.

Mitigation: Review the report content before submission and omit raw prompts, employee data, tokens, or complete API responses.

Risk: The release evidence flags version-check caching behavior for review.

Mitigation: Review version-check behavior during deployment and account for its local cache before approving the skill for managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/global-company-employee)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing developer portal](https://developer.upkuajing.com/)
- [UpKuaJing API pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Employee List API](references/company-employee-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a company ID, an UpKuaJing API key, and explicit user confirmation before fee-incurring calls.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
