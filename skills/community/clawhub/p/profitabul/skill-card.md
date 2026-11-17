## Description:

Real-time futures market intelligence, GEX/options flow analysis, trading signals, paper trading, backtesting, and live execution via MCP. Covers ES, NQ, SPX, NDX, QQQ, IWM, GC, SI, CL, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeurge](https://clawhub.ai/user/codeurge)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to connect agents to Profitabul market intelligence, GEX-derived levels, trading signals, historical analysis, backtesting, paper trading, and optionally live futures execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable live brokerage actions when configured, and the security evidence flags insufficient user-facing safeguards or warnings.

Mitigation: Default to paper trading, require explicit confirmation before live trade tools, use broker-side limits, and keep live execution disabled unless intentionally enabled.

Risk: The Profitabul API key grants access to the MCP endpoint and may be exposed through chats, logs, or commits.

Mitigation: Store PROFITABUL_API_KEY only in local environment configuration, avoid sharing it in prompts or source control, and rotate it if exposed.

Risk: Market signals and backtests can be misleading or unsuitable for a user's financial situation.

Mitigation: Treat outputs as analysis inputs rather than financial advice and review strategy assumptions before acting.

## Reference(s):

- [Profitabul Platform](https://profitabul.com)
- [Profitabul API Documentation](https://profitabul.ai/docs)
- [Profitabul Skill on ClawHub](https://clawhub.ai/codeurge/skills/profitabul)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; MCP tool results may include market data, signals, reports, backtests, and trade status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROFITABUL_API_KEY; live execution depends on broker enablement.]

## Skill Version(s):

0.3.1 (source: server release metadata; artifact frontmatter lists 0.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
