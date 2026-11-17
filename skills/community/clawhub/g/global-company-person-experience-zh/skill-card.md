## Description:

Queries Upkuajing's global company database for a person's work history timeline by person ID, including company, role, dates, status, and summary fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, sales teams, and hiring managers can use this skill to retrieve work-experience records for a known person ID, validate career history, enrich B2B contact profiles, and assess candidate or prospect background.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through local .env inspection or by pasting credentials into chat.

Mitigation: Use a protected environment variable or secret store, restrict permissions on ~/.upkuajing, and do not print or share API keys.

Risk: The skill can trigger paid queries, account lookups, recharge-order creation, and new-key flows.

Mitigation: Require explicit user confirmation before each paid query, recharge, new-key, or account-management action.

Risk: Error reports can include request context that may contain personal or sensitive data.

Mitigation: Redact personal data and credentials before submitting error reports, and send reports only after user approval.

Risk: Results depend on a third-party external service and may contain business-person profile data.

Mitigation: Use the skill only when the Upkuajing service is trusted and the requester is authorized to process the returned person data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/global-company-person-experience-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing API pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Work Experience List API Reference](references/person-experience-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include paginated work-experience records, fee details, and request identifiers from the Upkuajing API.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
