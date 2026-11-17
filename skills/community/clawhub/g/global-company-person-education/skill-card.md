## Description:

Queries UpKuaJing for person-level education history, including attended schools, degrees, majors, minors, GPA, summaries, pagination, fees, and request identifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, hiring managers, and background-screening workflows can use this skill to retrieve education-history records for a known person ID when validating applicant credentials. Users should obtain appropriate authorization before querying candidate data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries paid education-history data and can expose candidate records.

Mitigation: Require human approval before each paid query, confirm a legitimate screening purpose, and avoid printing unnecessary candidate data.

Risk: The skill can read or create a local API key file under ~/.upkuajing/.env.

Mitigation: Inject UPKUAJING_API_KEY through a secure secret manager where possible; if a local file is used, restrict file permissions and do not allow the agent to print the file.

Risk: Top-up and payment helper flows can initiate account funding actions.

Mitigation: Require separate explicit human approval before any top-up order or payment-page flow.

Risk: Error reports may include request context or candidate-related inputs.

Mitigation: Ask for human confirmation before sending error reports and minimize candidate data in the report context.

## Reference(s):

- [Education History List API](references/person-education-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing developer platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Education queries return paginated JSON records with billing metadata and request identifiers.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
