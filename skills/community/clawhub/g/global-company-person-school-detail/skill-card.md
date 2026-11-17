## Description:

Obtains detailed school information, including school type, location, websites, and social links, for institution verification and academic-network research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, researchers, analysts, and agents use this skill to look up detailed school records by school ID for degree verification, institutional research, academic network analysis, and data enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and may store an UpKuaJing API key locally.

Mitigation: Prefer an environment variable or a securely permissioned local file, and do not expose the key in chat, logs, or command output.

Risk: School lookup and account top-up flows can incur fees.

Mitigation: Confirm each fee-incurring query, top-up order, or paid account action with the user before execution.

Risk: Normal API calls also perform a version check against the UpKuaJing service.

Mitigation: Review the network behavior before installation and account for this additional outbound request in deployment policy.

## Reference(s):

- [School Detail API Reference](references/school-detail-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-person-school-detail)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; school lookups and account actions may incur fees and should be confirmed before execution.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
