## Description:

mx-financial-assistant provides Chinese-language financial Q&A, market data lookup, news and research retrieval, macroeconomic data tracking, asset screening, financial knowledge answers, and market analysis through Eastmoney's financial data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and financial research users use this skill to ask natural-language questions in Chinese about market data, company information, news, announcements, research reports, macroeconomic indicators, asset screening, and financial concepts. The skill returns a summarized answer with source references when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may route ordinary or non-financial Chinese-language questions to Eastmoney's external API.

Mitigation: Review the skill before installation and narrow activation criteria for deployments where unrelated questions or sensitive prompts may be entered.

Risk: User questions and any included account numbers, private portfolio details, or confidential trading plans may be sent to the external API provider.

Mitigation: Avoid submitting sensitive financial or personal information unless the deployment owner has approved sharing it with the provider.

Risk: The skill depends on a local EM_API_KEY and an unpinned httpx dependency.

Mitigation: Store the API key securely, rotate it if exposed, and pin dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/mx-financial-assistant)
- [Publisher profile](https://clawhub.ai/user/financial-ai-analyst)
- [Eastmoney financial Q&A API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/ask)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON containing a Markdown answer and reference metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY; supports standard mode and deep-think mode; answers are intended to be presented in Chinese.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
