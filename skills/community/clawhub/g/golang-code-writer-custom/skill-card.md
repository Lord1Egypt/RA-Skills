## Description:

Golang 开发 SKILL 集合，指导代理在 Golang 项目中编写日志、分析 API/MCP 运行流程，并生成代码示例、Mermaid 流程图和 Markdown 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[l2yf](https://clawhub.ai/user/l2yf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide Golang work that needs consistent logging, MCP client patterns, API flow analysis, error handling, and concise implementation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logging examples could encourage raw MCP request, response, token, or personal data logging in production systems.

Mitigation: Require redacted or allowlisted fields, avoid raw body dumps, truncate large responses, and review generated logging before production use.

Risk: MCP endpoint examples depend on local configuration and could target incorrect or untrusted services if copied without review.

Mitigation: Validate configured MCP endpoints, keep service URLs in configuration, and apply response-size limits plus explicit error handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/l2yf/skills/golang-code-writer-custom)
- [Publisher profile](https://clawhub.ai/user/l2yf)
- [SKILL-logging.md](artifact/SKILL-logging.md)
- [SKILL-flow-analysis.md](artifact/SKILL-flow-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Go code examples, Mermaid diagrams, configuration guidance, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP request patterns, logging statements, API flow summaries, and risk-aware production guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
