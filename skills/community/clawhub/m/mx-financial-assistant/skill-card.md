## Description: <br>
Provides Chinese-language financial Q&A backed by Eastmoney financial data, covering market data, financial news, macroeconomic data, screening, financial knowledge, market analysis, and event interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, financial analysts, and individual investors use this skill to ask Chinese-language questions about financial markets, financial data, market news, macroeconomic indicators, securities or fund screening, and financial concepts. It is intended for informational research support, not complete report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user questions to an external finance API and broad triggers could route unintended financial prompts to that service. <br>
Mitigation: Invoke it only when the user intentionally wants Eastmoney-backed financial Q&A, and review the prompt before sending it. <br>
Risk: Queries may contain secrets, account identifiers, private holdings, non-public business information, or proprietary research. <br>
Mitigation: Do not include sensitive credentials or private financial information unless the user is comfortable sharing that text with the external API. <br>
Risk: Stock, fund, allocation, or market-analysis outputs may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as informational research support and verify important decisions with qualified sources or advisors. <br>
Risk: The skill requires the EM_API_KEY credential. <br>
Mitigation: Store EM_API_KEY in the agent environment or secret manager and avoid printing or committing the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/mx-financial-assistant) <br>
- [Eastmoney financial Q&A API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/ask) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON from the helper script containing a Markdown answer and optional cited references; the agent should present the answer as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and sends user questions to the Eastmoney API; supports an optional deep-think mode.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
