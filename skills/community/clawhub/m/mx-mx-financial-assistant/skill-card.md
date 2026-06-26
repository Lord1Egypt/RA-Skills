## Description: <br>
Mx Financial Assistant answers financial questions in Chinese using Eastmoney financial data, market news, macroeconomic data, screening workflows, financial knowledge, and cited source references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akiry09](https://clawhub.ai/user/akiry09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial research workflows use this skill to ask natural-language questions about markets, securities, funds, bonds, macroeconomic indicators, financial news, and financial concepts. It is intended for informational research support and should not be treated as personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad financial-question triggers may route sensitive financial questions to the skill unexpectedly. <br>
Mitigation: Use the skill only for clearly financial questions that are appropriate for the Eastmoney-backed service. <br>
Risk: Questions are forwarded to a third-party financial service and may contain private portfolio, client, unpublished research, or trading-plan information. <br>
Mitigation: Avoid submitting sensitive financial details unless the user has approved that provider and its data handling. <br>
Risk: Financial answers may be interpreted as personalized investment advice. <br>
Mitigation: Treat outputs as informational research support and require qualified human review before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/akiry09/mx-mx-financial-assistant) <br>
- [Eastmoney financial assistant API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/ask) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON containing a Markdown answer and reference metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language responses; cited references may include data tables, news, announcements, and research reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
