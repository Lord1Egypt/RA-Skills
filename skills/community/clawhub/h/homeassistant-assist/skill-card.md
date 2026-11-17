## Description:

Controls Home Assistant smart-home devices by passing natural-language requests to the Assist (Conversation) API for intent parsing, entity resolution, execution, and response handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[developmentcats](https://clawhub.ai/user/developmentcats)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent control or query Home Assistant smart-home devices through Home Assistant's Assist API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad smart-home control through Home Assistant.

Mitigation: Review the skill before installation and avoid using it for locks, alarms, garage doors, or other high-risk devices unless additional confirmation is added.

Risk: The skill relies on a long-lived Home Assistant token.

Mitigation: Use a dedicated Home Assistant token with the least access available and protect the OpenClaw config file that stores it.

Risk: Requests may be sent to a Home Assistant server over an insecure transport if HASS_SERVER is misconfigured.

Mitigation: Prefer HTTPS for HASS_SERVER.

Risk: Concurrent or ambiguous smart-home commands can create unsafe device actions.

Mitigation: Add confirmation and safe request serialization before enabling control of high-risk devices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/developmentcats/skills/homeassistant-assist)
- [Home Assistant Conversation API Docs](https://developers.home-assistant.io/docs/intent_conversation_api/)
- [Home Assistant Long-Lived Access Tokens](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HASS_SERVER, HASS_TOKEN, and curl.]

## Skill Version(s):

1.1.1 (source: server release metadata and CHANGELOG, released 2026-02-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
