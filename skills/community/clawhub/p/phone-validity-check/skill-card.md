## Description:

Validates phone-number status, number type, and WhatsApp registration to help clean contact lists before outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, recruiters, traders, and exporters use this skill to check whether phone numbers are valid, whether they are landline or mobile numbers, and whether they are registered for WhatsApp before CRM cleanup, candidate screening, supplier verification, or bulk outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers and WhatsApp-status checks are sent to Upkuajing's paid external API.

Mitigation: Use the skill only for data you are authorized to validate, disclose that a paid external API is used, and require explicit confirmation before fee-incurring calls.

Risk: The skill can read or store UPKUAJING_API_KEY in a local ~/.upkuajing/.env file.

Mitigation: Prefer a secure environment or secrets manager; when using the local file, restrict file permissions and avoid sharing the key.

Risk: Error reports may include request context related to failed API calls.

Mitigation: Send error reports only after user confirmation and avoid including customer records, phone lists, or tokens in report context.

## Reference(s):

- [Phone Validity API](references/phone-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [Upkuajing Homepage](https://www.upkuajing.com)
- [Upkuajing Open Platform](https://developer.upkuajing.com/)
- [Upkuajing API Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/phone-validity-check)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation responses can include status, phone type, WhatsApp registration, country code, fee, balance, and request ID when returned by the API.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
