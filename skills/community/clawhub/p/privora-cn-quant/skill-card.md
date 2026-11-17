## Description:

Privora connects AI agents to a bearer-token investment workflow platform for A-share, Hong Kong, U.S., gold, fund, and financial-event data, plus Python backtesting, paper trading, portfolio attribution, cloud alerts, and workflow orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guangfuwu](https://clawhub.ai/user/guangfuwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI-agent operators use this skill to query market and portfolio data, run quantitative analysis and backtests, manage simulated trading workflows, and configure alerts through a Privora-issued bearer token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad Privora platform authority, including persistent remote changes.

Mitigation: Install it with a dedicated least-privilege Privora token, start with read-only scopes, and add write scopes only for a specific workflow.

Risk: Some scheduler, dependency, and plugin operations can replace persistent state and may not have enforced confirmation.

Mitigation: List current scheduler dependencies and plugin bindings first, then submit the complete intended state after operator review.

Risk: A bearer token grants access to the data and capabilities in its scopes, including sensitive portfolio data when those scopes are granted.

Mitigation: Treat the token as a secret, avoid giving it to untrusted agents, rotate it after exposure, and avoid wildcard or unrelated scopes.

Risk: Analysis, backtest, alert, and simulated-trading outputs can be incomplete, stale, or misleading if used without review.

Mitigation: Verify data freshness, strategy assumptions, and scope of results before acting; do not treat outputs as investment advice or live trading instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guangfuwu/skills/privora-cn-quant)
- [Privora Product Homepage](https://privora.cn)
- [Privora Data Coverage](https://privora.cn/features/realtime-minute-data-coverage)
- [Privora Token Management](https://privora.cn/profile/tokens)
- [Privora Marketplace](https://privora.cn/marketplace)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LG_AGENT_BASE_URL and LG_AGENT_TOKEN; available actions depend on the scopes granted to the Privora bearer token.]

## Skill Version(s):

1.0.57 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
