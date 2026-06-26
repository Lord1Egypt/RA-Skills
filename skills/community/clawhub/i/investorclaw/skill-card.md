## Description: <br>
Deterministic-first portfolio analyzer for holdings, performance, Sharpe and Sortino ratios, FRED yield curves, bond duration, sector breakdowns, and scenario rebalancing via MCP-HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perlowja](https://clawhub.ai/user/perlowja) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use InvestorClaw to connect an agent to a local portfolio-analysis service, load broker-export portfolio files, and ask for educational portfolio snapshots, performance windows, allocation analysis, and scenario rebalancing. Agents should source market figures from same-turn InvestorClaw tool results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service persists financial context and provider keys through local web and MCP surfaces. <br>
Mitigation: Install on a personal machine or tightly controlled localhost environment, review the Docker Compose file, and keep ports 18090 and 18092 bound to loopback. <br>
Risk: Remote dashboard exposure could disclose sensitive financial data if deployed without suitable controls. <br>
Mitigation: Avoid exposing the dashboard remotely without authentication; use a VPN, mTLS, or equivalent access control for any remote access. <br>
Risk: LLM narration can send portfolio-derived summaries to configured providers. <br>
Mitigation: Configure model providers intentionally, disclose this data flow to users, and prefer local model endpoints when portfolio privacy requirements demand it. <br>
Risk: Stored memory and response history may contain sensitive financial information. <br>
Mitigation: Treat memory and response history as sensitive data, and provide deletion or opt-out practices where the deployment requires them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/perlowja/investorclaw) <br>
- [Homepage from ClawHub Metadata](https://github.com/argonautsystems/InvestorClaw) <br>
- [MCP Tools Reference](artifact/docs/MCP_TOOLS_REFERENCE.md) <br>
- [Input Contract](artifact/docs/references/contract-input.md) <br>
- [Output Contract](artifact/docs/references/contract-output.md) <br>
- [Agent-Side Presentation Rules](artifact/docs/references/presentation-rules.md) <br>
- [Holdings Schema Field Reference](artifact/docs/references/schema-holdings-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP or REST tool calls and JSON result envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial figures should come from same-turn InvestorClaw tool results; outputs are educational and not investment advice.] <br>

## Skill Version(s): <br>
4.10.0 (source: server release metadata, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
