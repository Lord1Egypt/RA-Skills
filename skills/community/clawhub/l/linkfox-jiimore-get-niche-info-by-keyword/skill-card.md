## Description:

按关键词深度分析亚马逊细分市场，涵盖垄断程度、品牌集中度、新品成功率和市场机会评分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to query Jiimore niche-market data by keyword and compare demand, competition, brand concentration, advertising cost, launch success, and return-rate signals across supported marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect phone or SMS login data and depends on LinkFox API keys.

Mitigation: Use trusted environment variables, avoid exposing credentials in agent logs, and run onboarding only in a controlled environment.

Risk: The skill can create payment orders and consume paid compute for repeated market-data calls.

Mitigation: Confirm cost expectations before additional calls, rely on the built-in cache where appropriate, and require user approval before payment or repeated retrieval.

Risk: The skill stores full market-analysis responses locally and may send automatic feedback to a separate service.

Mitigation: Avoid sensitive product-research queries when logs or saved outputs may be shared, and review stored response files before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-jiimore-get-niche-info-by-keyword)
- [极目-亚马逊-细分市场信息 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are persisted under a linkfox session directory; small responses may be printed inline, while larger responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
