## Description: <br>
港股 AI 概念板块专属投研顾问。结合宏观流动性、南向资金博弈与 AI 产业基本面，提供深度的个股挖掘与风控策略。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangwenxin160-cpu](https://clawhub.ai/user/yangwenxin160-cpu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to structure Hong Kong AI-sector equity research around macro liquidity, southbound capital flows, industry catalysts, stock fundamentals, technical levels, and risk controls. It is intended for analytical support and data summarization, not licensed investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated equity research or action plans may be mistaken for licensed financial advice. <br>
Mitigation: Keep the artifact's investment-advice disclaimer visible and require users to verify conclusions with primary market data and qualified financial professionals. <br>
Risk: Market data, liquidity signals, and technical levels can be stale, incomplete, or provider-specific. <br>
Mitigation: Cross-check outputs against primary or trusted sources such as HKEX filings, official company reports, and current market-data providers before acting. <br>
Risk: The skill declares market-data and OpenAI API key environment variables. <br>
Mitigation: Use least-privilege credentials, avoid pasting secrets into prompts, and rotate keys if exposed. <br>
Risk: Read-only file access can still expose sensitive user-provided documents to analysis. <br>
Mitigation: Limit accessible files to documents intentionally selected for research and remove confidential material that is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangwenxin160-cpu/hk-ai-stock-expert) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown research analysis with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference market data sources and read-only user-provided files when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
