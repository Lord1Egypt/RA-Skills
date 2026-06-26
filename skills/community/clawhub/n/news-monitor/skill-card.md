## Description: <br>
Real-time news aggregator with Discord and Telegram push notifications for Jin10, BlockBeats, RSS, X KOLs, Polymarket, and OpenNews sources via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxcnny930](https://clawhub.ai/user/zxcnny930) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to install, configure, and operate a local real-time news monitoring service with REST API controls and Discord or Telegram notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill clones and runs an external Buzz repository. <br>
Mitigation: Install only when the external repository is trusted and review the cloned source before running it. <br>
Risk: An empty dashboard password leaves local API endpoints unauthenticated. <br>
Mitigation: Set a non-empty dashboard password before configuring feeds, notification channels, or tokens. <br>
Risk: Dashboard URLs containing the password query parameter can expose credentials if shared or logged. <br>
Mitigation: Avoid sharing URLs containing ?pw= and prefer local-only use of the dashboard. <br>
Risk: Discord, Telegram, X, and AI API credentials may be used by the local service. <br>
Mitigation: Protect tokens, use least-privilege credentials where possible, and rotate them if exposed. <br>
Risk: The monitoring service continues polling and pushing notifications while the Node process is running. <br>
Mitigation: Stop the Node process when monitoring is no longer desired. <br>


## Reference(s): <br>
- [News Monitor on ClawHub](https://clawhub.ai/zxcnny930/news-monitor) <br>
- [6551 MCP Token Setup](https://6551.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST API payloads and curl commands for a local dashboard.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
