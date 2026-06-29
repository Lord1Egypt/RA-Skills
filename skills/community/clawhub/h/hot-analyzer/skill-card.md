## Description: <br>
Hot Analyzer fetches public hot-list data from multiple Chinese platforms and analyzes potential sentiment effects on bonds, Shenwan industries, directly related securities, and futures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianchunhui](https://clawhub.ai/user/bianchunhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to collect public trend data, merge related hot-list items, score market relevance, and draft concise market-impact analysis. The analysis covers rate bonds, credit bonds, Shenwan industries, directly related listed instruments, and futures products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public hot-list endpoints operated by Toutiao, Baidu, Weibo, Douyin, and Zhihu. <br>
Mitigation: Run it only in environments where those outbound requests are acceptable and review network policy before use. <br>
Risk: The skill saves fetched public trend data and generated reports in the current workspace. <br>
Mitigation: Use a workspace where local raw JSON, state, grouping, HTML, and Markdown analysis files are expected and can be reviewed or removed. <br>
Risk: The skill generates financial-market conclusions from trend data and LLM reasoning. <br>
Mitigation: Treat conclusions as analysis rather than trading advice, and review market-impact claims before relying on them. <br>


## Reference(s): <br>
- [Hot Analyzer on ClawHub](https://clawhub.ai/bianchunhui/hot-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/bianchunhui) <br>
- [Toutiao Hot Board](https://www.toutiao.com/) <br>
- [Baidu Realtime Hot Board](https://top.baidu.com/) <br>
- [Weibo Hot Search](https://weibo.com/) <br>
- [Douyin Hot Search](https://www.douyin.com/) <br>
- [Zhihu Hot List](https://www.zhihu.com/hot) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown report, JSON intermediate files, shell commands, Python code, and an HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local workspace files such as raw platform JSON, state.json, pending.json, groups.json, and hot_analysis_report.html.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
