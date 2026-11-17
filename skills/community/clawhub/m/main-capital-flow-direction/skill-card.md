## Description:

牛股王独家研发的A股主力资金流向监测工具，基于主力资金净流入/流出数据，叠加上证指数走势，实时展示大资金进出方向，帮助投资者识别资金驱动力、捕捉资金与指数的背离信号，辅助择时决策，避免被表面行情误导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户和金融市场分析人员可用该 skill 查询A股主力资金流入/流出、个股和板块资金榜单，并结合上证指数走势识别资金与价格的背离信号。输出应作为市场信息和分析辅助，不应被视为投资建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market summaries may be mistaken for investment advice.

Mitigation: Treat outputs as informational, preserve the required AI disclaimer, and have users verify decisions against independent financial advice and current market data.

Risk: Responses include Niuguwang attribution and a promotional app/PC link.

Mitigation: Install or enable the skill only where that branded footer and link are acceptable to the workspace or end user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/main-capital-flow-direction)
- [Niuguwang CapitalFlows Index public API endpoint](https://stq.niuguwang.com/taoquant/CapitalFlows/Index?s=_test&version=6.9.5&packtype=1&night=0)
- [Niuguwang App and PC download page](https://www.stockhn.com/#/appDownload)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown text with market-data summaries, API field explanations, and required source and AI-disclaimer footer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a public Niuguwang GET endpoint without an API key; answers include Niuguwang attribution and an investment-risk disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
