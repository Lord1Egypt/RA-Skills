## Description:

Real-time news aggregator with Discord & Telegram push. Manage Jin10, BlockBeats, RSS, X KOLs, Polymarket, OpenNews via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxcnny930](https://clawhub.ai/user/zxcnny930)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use News Monitor to install and manage a local news aggregation service that collects market and crypto news sources and sends selected alerts to Discord or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run mutable Node.js code from an upstream repository.

Mitigation: Run it in an isolated directory or container, and pin and inspect the upstream repository before running npm install or npm start.

Risk: Sensitive configuration can be exposed if the dashboard password is empty or weak.

Mitigation: Set a non-empty dashboard password and keep the dashboard reachable only from trusted local or internal environments.

Risk: Bot tokens, webhook URLs, and API keys may be exposed through shell history or sent to third-party services during normal operation.

Mitigation: Avoid placing real secrets directly in command history, rotate exposed credentials, and confirm which Discord, Telegram, AI, RSS, and news services will receive configured content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxcnny930/skills/news-monitor)
- [Publisher profile](https://clawhub.ai/user/zxcnny930)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request bodies, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local REST API examples and operational guidance for hot-reloading news source, alerting, and dashboard settings.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
