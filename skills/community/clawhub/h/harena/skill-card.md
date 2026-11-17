## Description:

Harena connects AI assistants to an MCP trading-intelligence workbench for market monitoring, personalized news analysis, trading signals, and alerts covering crypto and US stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wall-e](https://clawhub.ai/user/wall-e)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Harena to add read-only market data, portfolio watchlist management, news feeds, trading-signal analysis, and alert workflows to AI assistants through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration answers and profile preferences can reveal investment interests and risk tolerance.

Mitigation: Review Harena's privacy terms before submitting questionnaire answers, watchlists, or profile preferences.

Risk: The OpenClaw example uses an unpinned `npx clawhub@latest` installer.

Mitigation: Prefer direct MCP configuration or review the package before running the installer, and do not execute it with elevated privileges.

Risk: Market summaries, alerts, and trading signals can be incomplete or misleading if treated as financial advice.

Mitigation: Use the skill for information gathering and require human review before making trading or investment decisions.

## Reference(s):

- [Harena Website](https://harena.world)
- [Harena Install Guide](https://www.harena.world/install)
- [Harena MCP Docs](https://www.harena.world/mcp/docs)
- [Harena MCP Discovery](https://www.harena.world/.well-known/mcp.json)
- [Harena ClawHub Release](https://clawhub.ai/wall-e/skills/harena)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market summaries, alerts, symbol analysis, watchlist updates, profile settings, and MCP connection configuration.]

## Skill Version(s):

0.3.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
