## Description: <br>
Privora gives AI agents Bearer Token access to multi-asset financial data, Python strategy backtesting, paper trading, cloud alerts, and workflow actions for A-share, Hong Kong stock, gold, fund, and earnings-event analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guangfuwu](https://clawhub.ai/user/guangfuwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, active traders, and developers use this skill to connect an AI agent to Privora for market-data lookup, portfolio analysis, strategy backtesting, paper-trading simulation, alert setup, and workflow execution. It is intended for operator-reviewed financial analysis and workflow automation, not autonomous investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read data and perform scoped Privora platform actions when supplied with a Bearer Token. <br>
Mitigation: Use a dedicated token with the minimum scopes needed, start read-only where possible, and rotate the token if it is exposed. <br>
Risk: Workflow execution, scheduler changes, portfolio or paper-trading writes, and webhook sends can create persistent or external side effects. <br>
Mitigation: Require operator confirmation before these actions and reserve autonomous execution for read-only or clearly idempotent operations. <br>
Risk: Financial analysis, backtests, paper-trading simulations, and alert evaluations may be incomplete, stale, or unsuitable for real-money decisions. <br>
Mitigation: Treat outputs as analytical inputs for human review, verify data freshness and assumptions, and keep live trading or irreversible financial decisions outside autonomous agent execution. <br>


## Reference(s): <br>
- [Privora product homepage](https://privora.cn) <br>
- [Privora token management](https://privora.cn/profile/tokens) <br>
- [ClawHub skill page](https://clawhub.ai/guangfuwu/skills/privora-cn-quant) <br>
- [Privora public agent skill version endpoint](https://privora.cn/api/public/agent/skill-version) <br>
- [Privora public agent capabilities endpoint](https://privora.cn/api/public/agent/capabilities) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands, JSON request examples, and API-result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LG_AGENT_BASE_URL and LG_AGENT_TOKEN; use least-privilege token scopes for the intended workflow.] <br>

## Skill Version(s): <br>
1.0.31 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
