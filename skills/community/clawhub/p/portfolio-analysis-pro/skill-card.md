## Description: <br>
股票持仓分析系统，用于管理股票投资组合，实时更新价格，分析盈亏，生成报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcsoftear](https://clawhub.ai/user/jcsoftear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to run a local stock portfolio dashboard for recording holdings, refreshing prices, analyzing gains and losses, and exporting portfolio reports. The skill also supports optional LLM-assisted portfolio analysis when the user configures a provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The portfolio web app exposes sensitive portfolio and LLM-key controls too broadly for safe default installation. <br>
Mitigation: Run it locally, bind the server to 127.0.0.1, restrict CORS, and add authentication before exposing it to any network. <br>
Risk: Portfolio data, logs, reports, and configured LLM API keys may contain sensitive financial or credential information. <br>
Mitigation: Protect portfolio.db, logs, and reports with local file permissions, back them up carefully, and avoid entering valuable API keys until key handling is hardened. <br>
Risk: AI analysis may send portfolio details to the configured model provider. <br>
Mitigation: Use only trusted providers, review provider privacy terms, and avoid sending confidential portfolio details unless that data sharing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcsoftear/portfolio-analysis-pro) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [项目介绍文档.md](artifact/项目介绍文档.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON API responses, Python snippets, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local SQLite data, operation logs, and report files when the portfolio system is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
