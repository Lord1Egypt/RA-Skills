## Description: <br>
Market monitoring and alert system for prices and news. Use when the user asks to watch a price, monitor market conditions, get notified when an asset hits a target, or keep an eye on breaking news. Covers any USDT-paired crypto and A-shares (real-time via TongDaXin). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hchen13](https://clawhub.ai/user/hchen13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent operators use Market Watch to register crypto, A-share, and market-news alerts that notify an agent when configured price or keyword conditions are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alert context and session routing metadata are stored locally for monitor and notification delivery. <br>
Mitigation: Avoid putting secrets in alert summaries, review session keys and reply targets before registering alerts, and cancel stale alerts when monitoring is no longer needed. <br>
Risk: Background monitors and the optional macOS watchdog can continue running after registration. <br>
Mitigation: Install the watchdog only when recurring launchd persistence is intended, and use the provided cancel and daemon management commands to stop old alerts and monitors. <br>


## Reference(s): <br>
- [Market Watch ClawHub Release](https://clawhub.ai/hchen13/market-watch) <br>
- [Exchange HTTP API Reference](references/exchange-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and alert configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can register local JSON alert records, manage background monitor processes, and trigger OpenClaw delivery commands.] <br>

## Skill Version(s): <br>
1.2.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
