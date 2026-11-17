## Description:

Queries LinkedIn employee records by company ID through the UpKuaJing Open Platform API, returning employee identifiers and job titles for recruiting, sales, and organizational analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, and B2B lead-generation specialists use this skill to retrieve employee lists and job titles for a known LinkedIn company ID. It supports talent mapping, team-structure analysis, organizational research, and lead qualification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an UpKuaJing API key and stores or reads it from the user's environment or local UpKuaJing configuration file.

Mitigation: Store the API key with restrictive permissions or a secret manager, and do not print configuration file contents in shared logs or transcripts.

Risk: Employee lookup calls and account top-up actions may incur costs.

Mitigation: Check current pricing through the documented pricing flow and require explicit user confirmation before paid queries or top-up actions.

Risk: Lookup requests, responses, or optional error reports may include sensitive company, employee, or account-related data.

Mitigation: Send only the minimum data needed for the lookup or report, confirm error reporting with the user first, and avoid including sensitive request or response data in reports.

Risk: The server security verdict is suspicious because the skill handles API keys and paid account actions that users should review before installation.

Mitigation: Install only if the user trusts UpKuaJing with LinkedIn employee lookup requests and accepts the billing and account-management behavior.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/linkedin-company-employee)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing developer platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Employee List API reference](references/linkedin-company-employee-list-api.md)
- [Skill Error Report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Employee-list responses include pagination data, job-title fields, fee metadata, and request identifiers when returned by the API.]

## Skill Version(s):

1.0.3 (source: SKILL.md metadata, server release evidence, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
