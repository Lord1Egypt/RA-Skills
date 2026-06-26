## Description: <br>
自动生成结构化的全球市场、政经和 AI 新闻情报汇总报告，并支持定向深度分析、情报分级和相关事件检测。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmsx000-cloud](https://clawhub.ai/user/gmsx000-cloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and analysts use this skill to generate Chinese-language markdown briefings about markets, geopolitics, macroeconomic events, and AI news. It is intended to help an agent gather current public information, classify significant events, and produce timestamped summaries with source attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated financial or geopolitical analysis may be incomplete, outdated, or unsuitable for direct decision-making. <br>
Mitigation: Treat generated analysis as informational, check timestamps and cited sources, and verify important claims before acting. <br>
Risk: Running the helper script contacts external CoinGecko and Yahoo Finance APIs. <br>
Mitigation: Run the script only in environments where public external API calls are permitted. <br>
Risk: The skill may browse public news and RSS sources that contain rapidly changing or unverified claims. <br>
Mitigation: Prefer source-attributed summaries and cross-check high-impact claims before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmsx000-cloud/global-intel-summary) <br>
- [Sample output](examples/sample-output.md) <br>
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true) <br>
- [Yahoo Finance Nasdaq chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/^IXIC) <br>
- [Yahoo Finance Dow chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/^DJI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese-language Markdown reports; helper script output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should include timestamps and source attribution; financial and geopolitical analysis should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and package.json; artifact frontmatter describes internal content version 3.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
