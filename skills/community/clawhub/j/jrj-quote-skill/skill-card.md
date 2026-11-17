## Description:

A股实时行情和历史K线数据查询，支持技术指标计算，用于获取股票、场内基金、指数的实时价格、历史K线，以及计算MA、MACD、KDJ、BOLL、RSI等技术指标。

This skill is for research and development only.

## Publisher:

[haomanjia](https://clawhub.ai/user/haomanjia)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI assistants use this skill to retrieve A-share real-time quotes, historical daily K-line data, and local technical indicators for market review, formatted tables, and quantitative-analysis workflows. The artifact states that market data and indicators are for learning and research support and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The kline script can send JRJ_API_KEY to an arbitrary HTTP or HTTPS endpoint if JRJ_API_URL is set.

Mitigation: Install only after review, use a JRJ_API_KEY acceptable for this environment, and leave JRJ_API_URL unset unless the destination is fully trusted; the publisher should remove or strictly validate endpoint overrides.

Risk: Market data and technical indicators can be mistaken for investment advice or predictions.

Mitigation: Present outputs as informational analysis support only and require users to make independent investment decisions.

Risk: Indicator calculations can be incomplete when the upstream response is truncated or insufficient warmup data is available.

Mitigation: Review truncation warnings, adjust limit or start-date parameters, and avoid relying on indicators until enough historical data is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haomanjia/skills/jrj-quote-skill)
- [JRJ Claw homepage](https://ai.jrj.com.cn/claw)
- [API interface reference](artifact/references/api-reference.md)
- [Technical indicators guide](artifact/references/indicators-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown tables, with shell command and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JRJ_API_KEY. The kline script can output JSON by default or Markdown when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
