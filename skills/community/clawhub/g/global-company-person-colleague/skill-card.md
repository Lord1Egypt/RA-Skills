## Description:

Find internal company teammates via company ID and personnel ID, returning colleague identifiers and job titles from UpKuaJing's global company database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, sales teams, and B2B lead generation specialists use this skill to look up a target employee's colleagues after obtaining the required company and person identifiers. It helps map organizational relationships and discover additional stakeholders, with each colleague query requiring explicit user confirmation because API calls incur fees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid UpKuaJing API key and contacts UpKuaJing services.

Mitigation: Confirm the user accepts paid API usage and third-party service contact before installation or execution.

Risk: The skill stores or reads credentials from ~/.upkuajing/.env.

Mitigation: Use a redacted credential presence check, avoid printing the credential file, and restrict the file permissions.

Risk: Colleague queries, top-up orders, and error reports can send user or account information to the platform.

Mitigation: Review every paid query, top-up order, and error report with the user before sending it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-person-colleague)
- [Publisher Profile](https://clawhub.ai/user/upkuajing)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Colleague List API Reference](artifact/references/person-colleague-list-api.md)
- [Skill Error Report API Reference](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; colleague queries return paginated colleague records with fee and request identifiers.]

## Skill Version(s):

1.0.5 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
