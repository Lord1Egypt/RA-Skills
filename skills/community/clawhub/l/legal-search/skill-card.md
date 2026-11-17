## Description:

AI法律数据库检索助手面向律师、法官助理、法务人员，提供法律法规检索、案例查证、类案分析，并可生成交互式HTML法律分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Legal practitioners, judicial assistants, and legal operations users use this skill to retrieve Chinese statutes and judicial cases, compare similar cases, and prepare structured legal research reports. Developers and agents can also use it to configure Yuandian or PKULaw data access and run the bundled report-generation scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a mutable third-party MCP package with an API key.

Mitigation: Install only when the Yuandian and PKULaw providers are trusted, and pin or otherwise verify the npm MCP server before use.

Risk: Provider API tokens may be exposed to third-party tooling or incur usage costs if mishandled.

Mitigation: Keep API tokens scoped, store them outside shared artifacts, rotate them if exposed, and review provider billing and access settings.

Risk: Generated HTML reports may contain unsanitized legal-data fields and sensitive legal research content.

Mitigation: Treat generated reports as sensitive files, avoid opening reports built from untrusted records until HTML escaping is added, and sanitize provider data before sharing reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/legal-search)
- [法律数据源 API 配置指南](references/api-guide.md)
- [元典开放平台](https://open.chineselaw.com/)
- [北大法宝 MCP](https://mcp.pkulaw.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, structured legal analysis text, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local HTML reports containing legal query results, case summaries, similar-case comparisons, and analysis guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
