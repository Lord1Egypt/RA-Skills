## Description: <br>
Controls Home Assistant smart home devices through the Assist (Conversation) API by forwarding natural-language requests to Home Assistant for intent parsing and execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevelopmentCats](https://clawhub.ai/user/DevelopmentCats) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and smart-home operators use this skill to let an OpenClaw agent control or query Home Assistant devices such as lights, switches, thermostats, covers, vacuums, and media players through Home Assistant Assist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent send broad, fire-and-forget commands to real Home Assistant devices. <br>
Mitigation: Require manual confirmation before commands that affect locks, doors, alarms, covers, climate controls, appliances, or other safety-sensitive devices. <br>
Risk: The Home Assistant token may allow more access than the agent needs. <br>
Mitigation: Use a dedicated least-privilege Home Assistant token and restrict which entities Assist can control. <br>
Risk: Home Assistant API traffic or credentials could be exposed if configured insecurely. <br>
Mitigation: Prefer HTTPS for HASS_SERVER and keep HASS_TOKEN out of chats, transcripts, and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DevelopmentCats/homeassistant-assist) <br>
- [Publisher profile](https://clawhub.ai/user/DevelopmentCats) <br>
- [Home Assistant Conversation API documentation](https://developers.home-assistant.io/docs/intent_conversation_api/) <br>
- [Home Assistant long-lived access token documentation](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and relayed Home Assistant response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus HASS_SERVER and HASS_TOKEN environment variables; forwards natural-language commands to the Home Assistant Assist API.] <br>

## Skill Version(s): <br>
1.1.1 (source: release metadata and changelog, released 2026-02-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
