## Description: <br>
Control and inspect Home Assistant via REST API for entities, states, services, scenes, scripts, and automations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hogar23](https://clawhub.ai/user/Hogar23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Home Assistant state and execute device, scene, script, and automation actions through scoped REST API helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real Home Assistant devices through a long-lived access token. <br>
Mitigation: Store HA_TOKEN outside the skill folder, run the self-check before actions, and keep confirmation enabled for locks, alarms, garage doors, and other high-impact actions. <br>
Risk: Public Home Assistant URLs and credentials can expose device control if handled carelessly. <br>
Mitigation: Prefer HTTPS for HA_URL_PUBLIC and do not commit private env files, tokens, hostnames, or generated entity maps containing sensitive home details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hogar23/home-assistant-control) <br>
- [Home Assistant Entity Map](references/entities.md) <br>
- [Home Assistant Naming Context](references/naming-context.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown or plain text with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, HA_TOKEN, and HA_URL_PUBLIC at runtime.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
