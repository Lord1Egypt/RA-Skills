## Description:

股票持仓分析系统，用于管理股票投资组合，实时更新价格，分析盈亏，生成报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcsoftear](https://clawhub.ai/user/jcsoftear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage stock holdings, refresh market prices, analyze portfolio profit and loss, and generate downloadable portfolio reports through a local Python and Flask application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated network access can expose private holdings and LLM configuration through the Flask APIs.

Mitigation: Run on localhost only until authentication and access controls are added; avoid LAN exposure for real portfolio data.

Risk: LLM API keys and provider endpoints may be stored or served through configuration APIs.

Mitigation: Do not enter valuable API keys until secret storage and configuration APIs are fixed; allow only trusted LLM providers and endpoints.

Risk: Portfolio edit and delete functions can modify or remove local holdings data.

Mitigation: Back up portfolio.db before using edit or delete functions, especially with real holdings.

Risk: Portfolio details may be sent to external LLM or market-data services.

Mitigation: Review external data flows and disclose them to users before enabling LLM analysis or live price updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcsoftear/skills/portfolio-analysis-pro)
- [README.md](artifact/README.md)
- [项目介绍文档.md](artifact/项目介绍文档.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON API responses, Python code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate Markdown portfolio reports and local Flask API responses backed by SQLite portfolio data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
