## Description:

Mx Financial Assistant answers Chinese-language financial questions by calling Eastmoney's financial data service for market data, financial news, macroeconomic data, screening, encyclopedia answers, market analysis, and cited references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akiry09](https://clawhub.ai/user/akiry09)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial research workflows use this skill to ask natural-language questions about market data, financial news, macroeconomic indicators, asset screening, and financial concepts. It returns Chinese Markdown answers with structured source references when the Eastmoney service provides them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial questions, investment interests, holdings typed by the user, and the Eastmoney API key are sent to Eastmoney's remote service.

Mitigation: Use only when that data sharing is acceptable, and avoid including personal identifiers or confidential portfolio details.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/akiry09/skills/mx-mx-financial-assistant)
- [Eastmoney financial Q&A API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/ask)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON containing a Markdown answer and structured references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and the httpx Python package; supports standard and deep-think modes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
