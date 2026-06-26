## Description: <br>
🌅 全时段股市资讯生成器。根据当前时间自动判断生成早报/午评/收盘报告，支持交易日检测、模块化新闻抓取、微信友好格式输出。专为投资人设计，助力快速决策。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and market watchers use this skill to generate Chinese A-share morning, midday, and closing reports from current public finance pages, recent news, and trading-day context. It is designed for fast situational awareness and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad global auto-load triggers can activate the skill during general finance conversations. <br>
Mitigation: Narrow or disable global auto-load triggers when the workflow should only run on explicit user request. <br>
Risk: Market reports can become misleading if current web data is unavailable, stale, or blocked by page verification. <br>
Mitigation: Use the skill's documented freshness checks, cite current public finance pages, and omit or label any data that cannot be verified. <br>
Risk: The workflow includes examples for saving Markdown, HTML, or PDF files to a fixed local path. <br>
Mitigation: Confirm the destination path and export format with the user before writing files or exporting PDF. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/poxiao) <br>
- [Eastmoney A-share quote center](https://quote.eastmoney.com/center/gridlist.html#hs_a_board) <br>
- [Eastmoney sector ranking](https://quote.eastmoney.com/center/boardrank.html) <br>
- [Eastmoney capital flow](https://data.eastmoney.com/zjlx/dpzjlx.html) <br>
- [Eastmoney market heatmap](https://quote.eastmoney.com/stockhotmap/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report with optional HTML or PDF export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include short market summaries, tabular market data, risk disclaimers, and optional local file output.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and artifact version table) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
