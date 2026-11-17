## Description:

全时段股市资讯生成器，根据当前时间自动判断并生成早报、午评或收盘报告，支持交易日检测、实时网页数据抓取、模块化新闻抓取和微信友好格式输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, market watchers, and analysts use this skill to generate Chinese A-share morning, midday, or closing market reports from current market pages and recent news. The reports are informational and should not be treated as personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad finance triggers can auto-start external browsing and report generation.

Mitigation: Narrow trigger conditions and require user confirmation before browsing or saving files.

Risk: The workflow may save generated reports to a hardcoded Desktop path.

Mitigation: Change the output directory to a user-approved workspace path and avoid overwriting existing files.

Risk: Generated reports may include buy, position, or market-timing suggestions.

Mitigation: Treat all trading-style language as informational, keep clear disclaimers, and avoid presenting it as personalized financial advice.

Risk: Financial and news data may be stale, incomplete, or blocked by third-party site protections.

Mitigation: Require current dated sources, cross-check important figures, and explicitly mark unavailable data rather than filling gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/poxiao)
- [东方财富行情中心](https://quote.eastmoney.com/center/gridlist.html#hs_a_board)
- [东方财富板块排行](https://quote.eastmoney.com/center/boardrank.html)
- [东方财富资金流向](https://data.eastmoney.com/zjlx/dpzjlx.html)
- [东方财富大盘星图](https://quote.eastmoney.com/stockhotmap/)
- [东方财富首页](https://www.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or HTML market reports, with optional local file output and PDF export guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates time-dependent A-share reports, may browse third-party finance/news sites, and may save report files to a local path.]

## Skill Version(s):

3.2.0 (source: release evidence and SKILL.md version table)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
