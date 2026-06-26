## Description: <br>
Analyze cryptocurrency, stock, and forex trading charts using GPTChart.ai's AI-powered technical analysis engine with basic and expert modes and GPTChart credit usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiasheng98](https://clawhub.ai/user/jiasheng98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agent operators use this skill to request GPTChart.ai technical analysis for crypto, stock, and forex symbols, then present market bias, price levels, reasoning, and credits used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GPTChart API key and analysis calls can consume GPTChart credits. <br>
Mitigation: Use a dedicated or easily rotated key, avoid exposing the key in logs or responses, and ask for confirmation before running batches of analyses. <br>
Risk: Custom prompts and analysis requests are sent to GPTChart.ai. <br>
Mitigation: Avoid sending sensitive personal, account, or trading information in prompts or symbols beyond what is needed for the analysis. <br>
Risk: Market analysis may be incomplete or unsuitable as the sole basis for trading decisions. <br>
Mitigation: Treat results as informational analysis, review the reasoning and price levels, and apply independent risk controls before acting. <br>


## Reference(s): <br>
- [GPTChart.ai](https://gptchart.ai) <br>
- [GPTChart API keys](https://gptchart.ai/account/api-keys) <br>
- [GPTChart pricing plan](https://gptchart.ai/account/pricing-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with optional shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GPTCHART_API_KEY; analysis calls can consume GPTChart credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
