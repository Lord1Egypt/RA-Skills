## Description:

Searches LinkedIn company data through the UpKuaJing Open Platform API using filters such as company name, industry, company size, founding year, geography, and contact-data availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams, marketers, B2B lead-generation specialists, and market researchers use this skill to find LinkedIn company profiles and enrich firmographic data for customer acquisition, account-based sales, competitor analysis, and target-client research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reads an UpKuaJing API key from the environment or `~/.upkuajing/.env`.

Mitigation: Keep the key out of chat and logs, restrict permissions on `~/.upkuajing/.env`, and rotate the key if it is exposed.

Risk: Searches and account top-up flows can incur fees.

Mitigation: Confirm pricing and obtain explicit user approval before paid searches, large result requests, or top-up order creation.

Risk: Search results may include company contact and firmographic data saved to local JSONL files.

Mitigation: Treat saved result files as sensitive lead data and share or retain them only according to the user's data-handling policy.

Risk: Automatic version checks contact the UpKuaJing service and cache version information locally.

Mitigation: Review this network behavior before installing in restricted environments.

## Reference(s):

- [LinkedIn Company List API](references/linkedin-company-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Portal](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/linkedin-company-search)
- [Publisher Profile](https://clawhub.ai/user/upkuajing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples and JSON/JSONL result data from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search scripts return a JSON summary containing task id, status, total hits, request id, result file path, and fee information in RMB cents; company records are appended to result.jsonl.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
