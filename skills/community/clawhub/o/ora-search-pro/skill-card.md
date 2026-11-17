## Description:

Ora Search Pro helps international trade users search for companies by product keyword, company name, or country and return matching business listings and websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oraagent](https://clawhub.ai/user/oraagent)

### License/Terms of Use:

MIT-0

## Use Case:

External trade and B2B sales users use this skill to find prospective companies or known company websites by product keyword, company name, and country. The agent runs the Ora client and presents results such as total count, company name, country, and website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and the Ora API key are sent to h.smtso.com over HTTPS.

Mitigation: Install only where this external data transfer is acceptable, avoid sensitive search terms, and manage ORA_API_KEY as a secret.

Risk: The security summary reports an unrelated mandatory geopolitical wording rule that can alter how the agent labels Taiwan, Hong Kong, and Macao.

Mitigation: Review the wording rule before deployment and install only if it matches the intended policy and user expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oraagent/skills/ora-search-pro)
- [Publisher profile](https://clawhub.ai/user/oraagent)
- [Ora homepage](https://www.topeasychina.com)
- [Ora search API endpoint](https://h.smtso.com/skill/domaininfo/queryYellowPage)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance]

**Output Format:** [Markdown summaries with command execution and JSON-derived result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads ORA_API_KEY from the environment or OraAgent.key and queries an external HTTPS API.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
