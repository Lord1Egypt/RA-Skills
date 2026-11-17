## Description:

Queries Juhe's enterprise information API by company-name keyword, registration number, or unified social credit code and returns matching enterprise records with company name, legal representative, founding date, registration number, and credit code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up enterprise business-registration list results through Juhe when a user provides a company keyword, registration number, or unified social credit code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Juhe API keys can be exposed if passed on the command line or embedded in copied URL examples.

Mitigation: Prefer the JUHE_ENTERPRISE_LIST_KEY environment variable and avoid placing keys in shell history, URLs, shared logs, or screenshots.

Risk: Enterprise search terms, registration numbers, or unified social credit codes are sent to Juhe's API.

Mitigation: Run lookups only when the user intends to query those identifiers and is comfortable sending them to Juhe.

Risk: Queries may consume paid or quota-limited Juhe API calls.

Mitigation: Confirm the lookup terms before execution and keep pagination within the documented page-size limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-list)
- [Juhe enterprise information API documentation](https://www.juhe.cn/docs/api/id/192)
- [Juhe data platform](https://www.juhe.cn)
- [Juhe enterprise simpleList API endpoint](https://japi.juhe.cn/enterprise/simpleList)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with shell command examples and formatted enterprise lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_ENTERPRISE_LIST_KEY API key; page size is capped at 20 results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
