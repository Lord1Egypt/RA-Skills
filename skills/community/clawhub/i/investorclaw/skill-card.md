## Description:

Deterministic-first portfolio analyzer for holdings, performance, Sharpe and Sortino, FRED yield curves, bond duration, sector breakdowns, and scenario rebalancing over MCP-HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perlowja](https://clawhub.ai/user/perlowja)

### License/Terms of Use:

MIT-0

## Use Case:

Portfolio owners, advisors, and developers use this skill to connect an MCP-capable agent to a local InvestorClaw container for read-only portfolio analysis, market snapshots, performance reporting, and educational rebalancing scenarios. Agents should use same-turn InvestorClaw tool results as the source of truth and avoid personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive unauthenticated management surfaces may expose portfolio data if the local MCP or dashboard ports are reachable by another user, browser page, container, or remote host.

Mitigation: Install on a personal machine, keep ports bound to loopback, and place an auth proxy or VPN in front of the service before any remote or shared deployment.

Risk: Provider keys and uploaded portfolio files are sensitive local assets.

Mitigation: Treat keys and portfolio files as sensitive, store only what is needed, and rotate keys if any local endpoint may have been reachable outside the intended user context.

Risk: Install and runtime weaknesses require review before use.

Mitigation: Prefer the bundled compose.yml, review deployment settings before install or upgrade, and avoid leaving the service running while browsing untrusted sites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perlowja/skills/investorclaw)
- [InvestorClaw homepage](https://github.com/argonautsystems/InvestorClaw)
- [MCP tools reference](artifact/docs/MCP_TOOLS_REFERENCE.md)
- [Privacy policy](artifact/PRIVACY.md)
- [Security policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with MCP tool calls, shell commands, configuration snippets, and JSON-derived portfolio analysis responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only educational analysis; numerical claims should come from same-turn InvestorClaw tool results.]

## Skill Version(s):

4.10.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
