## Description: <br>
Fetches China-market financial data and investment-research information across A-shares, Hong Kong stocks, funds, indices, financial statements, announcements, research reports, macroeconomic data, and related datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search InvestToday endpoints, call the `investoday-api` CLI, and summarize or export structured financial datasets for research, comparison, and analysis. It is not intended for direct buy or sell recommendations, automated trading, order execution, or invented conclusions when data is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a remote financial API and may send financial queries, chart text, or other user-provided inputs to that service. <br>
Mitigation: Install and use it only when the InvestToday API package and service are trusted, and avoid submitting confidential, personal, legal, or regulated data without appropriate controls. <br>
Risk: API keys or credentials could be exposed if pasted into shell commands, shared transcripts, or logs. <br>
Mitigation: Use safer secret handling for API keys and avoid placing real credentials directly in commands or shared conversation history. <br>
Risk: Trading signals and investment analysis can be incomplete, incorrect, delayed, or unsuitable for a user's circumstances. <br>
Mitigation: Treat outputs as informational, verify results against primary sources, and do not use the skill as a substitute for professional investment advice or trade execution controls. <br>
Risk: The server security review marked the release as needing review because of sensitive-looking sample data, repeated incorrect examples, and weak credential or privacy guidance. <br>
Mitigation: Review the skill documentation, endpoint examples, credential handling, and privacy posture before deployment. <br>


## Reference(s): <br>
- [InvestToday Finance Data ClawHub Page](https://clawhub.ai/kenneth-bro/investoday-finance-data) <br>
- [English Skill Overview](artifact/SKILL_EN.md) <br>
- [Reference Index](artifact/docs/references-index.en.md) <br>
- [基础数据](artifact/references/基础数据.md) <br>
- [市场数据](artifact/references/市场数据.md) <br>
- [沪深京数据证券资料](artifact/references/沪深京数据/基础信息/证券资料.md) <br>
- [沪深京数据实时行情](artifact/references/沪深京数据/股票行情/实时行情.md) <br>
- [沪深京数据财务当期指标数据](artifact/references/沪深京数据/财务数据/财务当期指标数据.md) <br>
- [基金概况](artifact/references/基金/基金资料/基金概况.md) <br>
- [指数资料](artifact/references/指数/指数资料.md) <br>
- [宏观经济国内宏观](artifact/references/宏观经济/国内宏观.md) <br>
- [研报基础数据](artifact/references/研报/基础数据.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured financial data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and the `@investoday/investoday-api` package; results depend on network access, API permissions, and endpoint coverage.] <br>

## Skill Version(s): <br>
1.8.31 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
