## Description:

Market monitoring and alert system for prices and news. Use when the user asks to watch a price, monitor market conditions, get notified when an asset hits a target, or keep an eye on breaking news. Covers any USDT-paired crypto and A-shares (real-time via TongDaXin).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hchen13](https://clawhub.ai/user/hchen13)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agents use this skill to register crypto, A-share, and market-news alerts, run background monitors, and notify the agent when alert conditions are met so it can follow up with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background monitors can continue polling market and news sources and can proactively message the agent after registration.

Mitigation: Start monitors only for intended alerts, cancel alerts that are no longer needed, and stop the daemon when monitoring is complete.

Risk: Alert records may store context summaries plus session and transcript references in local OpenClaw private state.

Mitigation: Provide explicit session and transcript parameters only when needed, keep alert summaries minimal, and review local private alert files before sharing logs or state.

Risk: The skill makes outbound calls to exchange, market-data, and news APIs, including unofficial Jin10 and Wallstreetcn interfaces that may change behavior.

Mitigation: Use a virtual environment with pinned dependencies, review the listed API endpoints, and expect graceful degradation or missed alerts when upstream formats change.

Risk: The optional macOS launchd watchdog can restart monitors automatically after a crash.

Mitigation: Avoid installing the watchdog unless restart persistence is required, and uninstall it when persistent monitoring is no longer desired.

## Reference(s):

- [Exchange HTTP API Reference](references/exchange-api.md)
- [OpenClaw](https://github.com/openclaw)
- [Market Watch ClawHub Skill Page](https://clawhub.ai/hchen13/skills/market-watch)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text alert messages; alert state is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local background monitors and sends proactive agent-delivered alerts when configured price or news conditions match.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
