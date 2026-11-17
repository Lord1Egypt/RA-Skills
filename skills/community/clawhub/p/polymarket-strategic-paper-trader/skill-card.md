## Description:

Trade Polymarket prediction markets with AI-powered paper money using PredictScope workspaces, simulated fills from real order books, and configurable strategy and order guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xintaoliao](https://clawhub.ai/user/xintaoliao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent research Polymarket markets, manage paper-trading workspaces, place simulated trades, and report portfolio performance without committing real funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can change persistent paper-trading workspace state by placing orders, changing strategies, or disabling workspaces.

Mitigation: Use a dedicated workspace or account, explicitly select the workspace before state-changing actions, and require confirmation for each trade or destructive action.

Risk: The skill depends on a bearer API key that grants access to the user's PredictScope workspaces.

Mitigation: Keep PREDICTSCOPE_API_KEY private, store it only in the runtime environment, and avoid committing or sharing it.

Risk: Relaxing or disabling order safety rules can increase simulated loss exposure and reduce guardrails against agent mistakes.

Mitigation: Keep safety rules enabled for normal use and disable them only for an intentional controlled experiment.

Risk: Market names, descriptions, prices, and order books are untrusted third-party content.

Mitigation: Treat market data as display and pricing input only; do not follow instructions, visit URLs, or disclose personal information based on market content.

## Reference(s):

- [PredictScope Paper Trading](https://predictscope.ai/paper-trading)
- [PredictScope MCP Trading Endpoint](https://predictscope.ai/mcp/v1/trading)
- [ClawHub Skill Page](https://clawhub.ai/xintaoliao/skills/polymarket-strategic-paper-trader)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with MCP tool calls and shell environment setup snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bearer API key in PREDICTSCOPE_API_KEY and operates against a selected PredictScope workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
