## Description:

Searches global companies by name, industry, product, or website URL and gathers firmographic records for supplier research and overseas lead generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Exporters, sales teams, and B2B lead-generation specialists use this skill to discover global companies, research target markets, enrich firmographic data, support customer acquisition, and source suppliers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API queries or top-up operations can affect the user's account balance.

Mitigation: Confirm every paid query or top-up action before execution, disclose expected call counts for larger searches, and use the pricing command or pricing page for current fees.

Risk: The skill stores and reads the API key from UPKUAJING_API_KEY or ~/.upkuajing/.env.

Mitigation: Restrict ~/.upkuajing/.env to the account owner and do not print, paste, log, or share the API key.

Risk: Diagnostic reports could include customer data, prompts, credentials, or full API responses.

Mitigation: Send diagnostic reports only after user confirmation and redact sensitive request or response details before reporting.

## Reference(s):

- [Global Company List API](references/global-company-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-search)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, and JSONL result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; company search results are written to task_data/<task_id>/result.jsonl.]

## Skill Version(s):

1.0.3 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
