## Description: <br>
Control Home Assistant devices and automations via REST API, including lights, climate, locks, presence, weather, calendars, notifications, scripts, and other smart-home entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anotb](https://clawhub.ai/user/anotb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and smart-home operators use this skill to let an agent inspect and control a Home Assistant instance through REST API calls. It supports device discovery, state reads, service calls, automations, scripts, notifications, calendars, history, and safety-confirmed actions for sensitive devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent read from and control a Home Assistant setup, including sensitive home devices. <br>
Mitigation: Install only when agent access to Home Assistant is intended, use a least-privileged Home Assistant token, protect HA_TOKEN like a password, and revoke it when no longer needed. <br>
Risk: Commands may affect locks, alarms, garage doors, gates, security automations, presence or location data, calendars, history, logbook data, scripts, scenes, or broad service calls. <br>
Mitigation: Require explicit user confirmation before executing actions involving sensitive devices, private data, or broad Home Assistant service calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anotb/homeassistant-skill) <br>
- [Skill homepage](https://github.com/anotb/homeassistant-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with bash, curl, jq, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HA_URL, HA_TOKEN, curl, jq, and network access to the user's Home Assistant instance.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
