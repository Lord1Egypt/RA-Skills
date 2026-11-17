## Description:

Checks LinkedIn work history by personnel ID and returns employers, job titles, employment dates, and status data from UpKuaJing LinkedIn datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, sales teams, and talent acquisition teams use this skill to review a professional's employment timeline when they have a valid UpKuaJing API key and authorization to query the person data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an UpKuaJing API key and may read credentials from a local secret file.

Mitigation: Prefer an environment variable or tightly permissioned secret file, and do not ask the agent to print ~/.upkuajing/.env.

Risk: LinkedIn employment-history queries and optional diagnostics may send person identifiers, request details, or response context to UpKuaJing.

Mitigation: Confirm authorization before candidate or person lookups, and minimize personal data included in any error report.

Risk: API calls, account actions, and paginated lookups can incur charges.

Mitigation: Review pricing and balance before use, and require explicit user confirmation before paid queries or top-up flows.

Risk: The security review notes account/payment actions and under-disclosed platform calls that users should review before installing.

Mitigation: Review the authentication, payment, version-check, and error-report behaviors before enabling the skill in a production agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-person-experience)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [Work Experience List API](artifact/references/linkedin-person-experience-list-api.md)
- [Skill Error Report API](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and formatted JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; successful queries include work-experience data, fee information, and a requestId.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
