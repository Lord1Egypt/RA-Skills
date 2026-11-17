## Description:

This skill uses the UpKuaJing Open Platform to query a person's work-experience records by personnel ID; server security evidence notes that the release metadata advertises education verification instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, hiring managers, and other authorized users can use this skill to request person work-experience records from UpKuaJing by personnel ID. Reviewers should resolve the documented mismatch between the education-verification release metadata and the artifact behavior before relying on it for screening workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release metadata advertises education verification, but the artifact queries work-experience records.

Mitigation: Confirm the intended data category before use and install only if the needed workflow is employment-history lookup.

Risk: The skill processes personal employment data by personnel ID.

Mitigation: Use it only with appropriate authorization and handle returned records under applicable privacy and hiring-screening policies.

Risk: The skill uses UPKUAJING_API_KEY and references ~/.upkuajing/.env.

Mitigation: Store the API key with restrictive permissions or a credential manager, and do not print the environment file in agent-visible output.

Risk: API queries and account top-up actions can incur costs.

Mitigation: Require explicit user confirmation before paid queries, top-up order creation, or payment-related actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-person-experience)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Work Experience List API](references/person-experience-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid API calls may return paginated records, fee information, and request identifiers.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
