## Description:

股票分析 AI 工具 | 智能投资简报生成器 - 自动生成个股分析报告、市场热点追踪、持仓监控。支持 A股/港股/美股，实时股价查询，技术分析，研报生成。一键生成专业 Markdown 投资报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use this skill to generate stock, market, and portfolio-oriented investment briefs from Tavily-powered search results. It is intended for concise Markdown reporting across A-share, Hong Kong, and U.S. equity contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted stock symbols or names may be executed as local shell commands.

Mitigation: Accept only trusted inputs until shell-string execution is replaced with argument-array execution and input validation.

Risk: The external Tavily search script receives the full environment.

Mitigation: Pass only required environment variables to child processes, especially TAVILY_API_KEY.

Risk: The Tavily search dependency is external to this artifact.

Mitigation: Pin or vendor the dependency and review it before deployment.

Risk: Investment briefs may contain incomplete or stale market information from external search results.

Mitigation: Require human review and independent source checks before using generated briefs for investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/investment-brief-generator)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown investment brief emitted to stdout or written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; generated reports depend on external search results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
