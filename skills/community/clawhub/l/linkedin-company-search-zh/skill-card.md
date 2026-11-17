## Description:

Searches LinkedIn company data by company name, industry, company size, founding year, location, and contact availability to support prospecting, market research, competitor analysis, and account-based sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, marketers, B2B lead builders, and agents use this skill to find and enrich LinkedIn company profiles for customer development, market research, competitor analysis, and account-based selling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Upkuajing's API service.

Mitigation: Use the skill only when sending the requested company-search criteria to Upkuajing is acceptable for the user and organization.

Risk: The skill can initiate paid API searches and payment-order flows.

Mitigation: Confirm expected paid searches, recharges, and high-volume requests before execution.

Risk: API keys and task result data may be stored locally.

Mitigation: Prefer environment variables or a secret store, do not print `.env` contents in chat or logs, and restrict permissions on `~/.upkuajing` and task data.

Risk: Error reports may include request or response details.

Mitigation: Submit error reports only after user confirmation and avoid including unnecessary sensitive information.

Risk: The security summary notes an undisclosed version-check cache.

Mitigation: Review version-check behavior and local cache contents before installation in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-company-search-zh)
- [Publisher profile](https://clawhub.ai/user/upkuajing)
- [Upkuajing homepage](https://www.upkuajing.com)
- [LinkedIn company list API reference](artifact/references/linkedin-company-list-api.md)
- [Skill error report API reference](artifact/references/skill-error-report-api.md)
- [Upkuajing OpenAPI price page](https://www.upkuajing.com/web/openapi/price.html)
- [Upkuajing developer platform](https://developer.upkuajing.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, and local JSONL result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid searches may store task results locally.]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
