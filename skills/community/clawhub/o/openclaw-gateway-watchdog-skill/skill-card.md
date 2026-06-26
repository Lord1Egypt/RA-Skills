## Description: <br>
Monitor OpenClaw gateway health with a watchdog state machine, Discord alerts, cooldown dedupe, and isolated fallback deployment on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw Gateway health, reduce noisy Discord alerts, and coordinate bounded recovery actions when Gateway service checks fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog may modify OpenClaw configuration or restart Gateway services automatically when alert conditions are met. <br>
Mitigation: Before scheduling it, set GW_WATCHDOG_AUTO_HEAL_ON_ALERT=0 and GW_WATCHDOG_AUTO_ROLLBACK_ON_CONFIG_INVALID=0 unless automatic repair, rollback, and restart behavior is explicitly desired. <br>
Risk: Discord webhook URLs, bot tokens, channel IDs, and incident details may be exposed if local configuration is mishandled. <br>
Mitigation: Protect config.env as a secret, avoid committing it, and use minimum required Discord permissions for the configured delivery path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonathanJing/openclaw-gateway-watchdog-skill) <br>
- [Publisher profile](https://clawhub.ai/user/JonathanJing) <br>
- [Cron Agent Turn Template](references/cron-agent-turn.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and operational status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Discord incident notifications, watchdog state files, event logs, and local configuration guidance when executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, skill.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
