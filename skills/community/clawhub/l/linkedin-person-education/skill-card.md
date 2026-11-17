## Description:

Check LinkedIn-sourced education history by personnel ID, including institutions, degrees, majors, minors, GPAs, and summaries for candidate screening and background verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, hiring managers, and authorized agents use this skill to retrieve LinkedIn-sourced education records by personnel ID for candidate screening, background verification, and talent assessment. It can also guide account setup, pricing checks, pagination, and error reporting for the UpKuaJing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs background-check style education lookups against UpKuaJing and may expose candidate-related query data to that service.

Mitigation: Install and run it only when authorized to perform these lookups and when the organization's privacy and hiring-review requirements are satisfied.

Risk: Queries may incur fees, including additional charges for paginated requests.

Mitigation: Check current pricing through the documented price flow and obtain explicit user confirmation before running any fee-incurring query.

Risk: The API key can be stored in a local plaintext env file and could be exposed through chat, logs, or loose file permissions.

Mitigation: Use a secret manager or restricted file permissions, avoid printing the key, and rotate any key that was exposed.

## Reference(s):

- [LinkedIn Person Education List API](artifact/references/linkedin-person-education-list-api.md)
- [Skill Error Report API](artifact/references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/linkedin-person-education)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Portal](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Publisher Profile](https://clawhub.ai/user/upkuajing)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid queries require explicit user confirmation before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
