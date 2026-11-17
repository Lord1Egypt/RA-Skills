## Description:

Portfolio Tool-基金组合研究工具 lets agents use natural-language workflows to query fund portfolios, sync fund NAV data, inspect tracking status, search funds, and manage anonymous account access through the portfolio-tool MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengkane](https://clawhub.ai/user/dengkane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a fund portfolio research backend from an agent conversation, including portfolio reads and writes, fund lookup, NAV synchronization, account binding, and recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived device-derived identifier as an account credential and stores it locally.

Mitigation: Treat ~/.portfolio/aid and any X-Anonymous-Id header value as credentials, and avoid sharing them across users or logs.

Risk: The skill can perform portfolio and account write operations through MCP or the fallback CLI.

Mitigation: Review intended tool calls before execution, especially create, update, delete, bind, login, password, and sync operations.

Risk: The fallback CLI accepts request bodies through command-line arguments, which can expose secrets such as passwords in shell history or process listings.

Mitigation: Avoid entering real passwords in documented --data command-line examples; prefer a safer client flow for sensitive credentials.

Risk: The fallback CLI sends requests to the configured PORTFOLIO_API backend.

Mitigation: Confirm PORTFOLIO_API points to the intended trusted backend before using the CLI fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengkane/skills/portfolio-tool)
- [Portfolio backend](https://invest.geeyo.com)
- [Streamable HTTP MCP endpoint](https://invest.geeyo.com/mcp/http)
- [SSE MCP endpoint](https://invest.geeyo.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON-oriented API output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use MCP tools first and a local Python CLI fallback when MCP is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
