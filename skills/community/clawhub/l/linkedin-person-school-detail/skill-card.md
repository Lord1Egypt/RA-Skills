## Description:

Pull detailed school information from LinkedIn data to help verify educational institutions and enrich academic network research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, researchers, analysts, and developers use this skill to fetch a school's name, type, location, website, and social links from a LinkedIn school ID for education verification, institutional research, and data enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billable API calls can spend account balance.

Mitigation: Inform the user that the lookup incurs a fee and wait for explicit confirmation before running billable queries or top-up actions.

Risk: The skill handles an UpKuaJing API key and may store it in a local .env file.

Mitigation: Use a dedicated low-balance API key and avoid printing or sharing the full .env file.

Risk: Error reports may send request context or response details to the provider.

Mitigation: Submit error reports only after user confirmation and omit sensitive request or response data unless the user accepts that disclosure.

Risk: The skill includes provider version-check behavior during API flows.

Mitigation: Review the outbound version-check behavior before installation and account for provider network calls during use.

## Reference(s):

- [LinkedIn School Detail API](artifact/references/linkedin-school-detail-api.md)
- [Skill Error Report API](artifact/references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Portal](https://developer.upkuajing.com/)
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [UpKuaJing OpenAPI Endpoint](https://openapi.upkuajing.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; billable lookup calls require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
