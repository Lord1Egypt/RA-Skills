## Description: <br>
Ora外贸客户开发专家 helps foreign-trade users search by country, company name, or product keyword to generate lists of relevant companies and websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oraagent](https://clawhub.ai/user/oraagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade and business-development users use this skill to find potential customer companies, websites, and company-list results from country, product, or company-name queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run inline local Node.js code and use a local OraAgent.key to call the h.smtso.com service. <br>
Mitigation: Install only if the publisher and service are trusted, confirm that the key is intended for this service, and prefer platform-managed secrets or a constrained HTTP tool where available. <br>
Risk: Search terms for customer development may expose sensitive customer, market, or strategy information to a third-party endpoint. <br>
Mitigation: Avoid entering sensitive terms unless the service's data-sharing terms are acceptable, and use broader non-sensitive keywords when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oraagent/ora-search-pro) <br>
- [Ora homepage](https://www.topeasychina.com) <br>
- [Ora customer-search API endpoint](https://h.smtso.com/skill/domaininfo/queryYellowPage) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown tables and concise guidance, backed by a form-encoded HTTPS API request.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries can use company name, product keyword, country code, page, and limit; the documented maximum is 1000 returned records.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
