## Description:

Search LinkedIn professionals with name, company, and job-title filters to fetch profile information for headhunting and global sales lead development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, and B2B lead-generation specialists use this skill to find LinkedIn-derived people records by name, company, job title, industry, geography, and contact-data availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and account data may be exposed if stored or displayed carelessly.

Mitigation: Use a protected environment variable or secret store where possible; if using `~/.upkuajing/.env`, restrict the directory and file to owner-only permissions and do not print or paste the file contents.

Risk: LinkedIn-derived people and contact data may be sensitive or regulated.

Mitigation: Use the skill only with a lawful basis for processing the data, limit access to result files, and avoid unnecessary retention or redistribution.

Risk: Search and account-management API calls may incur fees.

Mitigation: Check current pricing and obtain explicit confirmation before paid searches, especially when the requested result count requires multiple calls.

Risk: Error reports may accidentally include raw search parameters, responses, profile data, or credentials.

Mitigation: Review and redact error-report context before submission; do not include credentials or raw profile/contact data.

## Reference(s):

- [LinkedIn Person List API](references/linkedin-person-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/linkedin-person-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus JSON status and JSONL result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are written as task-scoped JSONL files, and script responses include task status, request identifiers, file paths, and fee information.]

## Skill Version(s):

1.0.3 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
