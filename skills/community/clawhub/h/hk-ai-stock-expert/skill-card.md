## Description:

港股 AI 概念板块专属投研顾问。结合宏观流动性、南向资金博弈与 AI 产业基本面，提供深度的个股挖掘与风控策略。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangwenxin160-cpu](https://clawhub.ai/user/yangwenxin160-cpu)

### License/Terms of Use:


## Use Case:

External research users use this skill to structure Hong Kong AI-sector equity analysis around liquidity, southbound capital flows, catalysts, fundamentals, technical levels, and risk controls. Outputs are research support and must not be treated as direct investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests raw API credentials, including MARKET_DATA_API_KEY and OPENAI_API_KEY, without documenting a specific need for each credential.

Mitigation: Review before installing, use a dedicated low-privilege market-data key when needed, and avoid granting OPENAI_API_KEY unless the publisher documents why it is required.

Risk: The skill produces finance research that could be mistaken for direct trading advice.

Mitigation: Treat outputs as research support only, verify claims against current market data, and preserve the skill's non-advisory investment disclaimer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangwenxin160-cpu/skills/hk-ai-stock-expert)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research analysis with structured sections and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference market data sources and user-provided tickers; outputs should remain analytical and non-advisory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
