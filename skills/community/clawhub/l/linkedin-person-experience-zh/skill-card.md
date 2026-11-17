## Description:

Retrieves a LinkedIn person's employment history by person ID through the Upkuajing API, including company names, job titles, start and end dates, and employment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, sales teams, and due diligence users can review a LinkedIn profile's work history by person ID, optionally filtered by company, to assess professional experience and career movement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid external API and paginated lookups may incur repeated charges.

Mitigation: Confirm expected costs before each paid lookup and use the pricing helper or published pricing page instead of estimating fees.

Risk: The skill reads or creates an Upkuajing API key in ~/.upkuajing/.env.

Mitigation: Use a scoped environment variable or securely permissioned credential file, and avoid sharing credential-file contents in chats or logs.

Risk: The helper script can create recharge or payment URLs.

Mitigation: Only open or act on payment links after the user explicitly requests account recharge.

Risk: Error reports may include request, response, or context data.

Mitigation: Review report contents and obtain user confirmation before submitting an error report.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/linkedin-person-experience-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [LinkedIn person experience list API reference](references/linkedin-person-experience-list-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; API lookups are paginated and may incur per-call charges.]

## Skill Version(s):

1.0.2 (source: server evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
