## Description:

全球大宗商品行情简报工具，支持查询伦敦金、伦敦银、伦敦铜、纽约铂、布伦特原油的当前价格和当日涨跌幅，生成简洁的行情简报。基于akshare获取实时数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[m0dzer0](https://clawhub.ai/user/m0dzer0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current precious-metals and Brent crude oil prices, inspect daily movement, and generate concise market briefings. The data is for public market reference and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires unpinned Python packages for data fetching.

Mitigation: Install it only in an environment where the current ClawHub installer and unpinned Python dependencies are acceptable.

Risk: Returned commodity prices may be stale, unavailable, or delayed by market hours, holidays, network errors, or upstream rate limits.

Mitigation: Check the reported data time, retry later after failures, and treat results as reference data rather than a guaranteed live trading feed.

Risk: Users may mistake public market summaries for investment advice.

Mitigation: Keep the reference-only framing and avoid presenting the output as a recommendation to trade or invest.

## Reference(s):

- [AkShare](https://github.com/akfamily/akshare)
- [Global Commodity Today on ClawHub](https://clawhub.ai/m0dzer0/skills/global-commodity-today)
- [m0dzer0 ClawHub profile](https://clawhub.ai/user/m0dzer0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown market briefing or single-commodity summary with inline shell commands for invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; commodity prices are in USD and include fetch time, latest price, daily change, open, high, low, and reference-only disclaimer when available.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
