## Description:

Control Home Assistant entities via REST API for climate, lights, switches, and sensor queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent find Home Assistant entities, query sensor state, and control lights, switches, and climate devices through the Home Assistant REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and sends a long-lived Home Assistant token that can control home devices.

Mitigation: Use a limited, revocable token where possible, avoid administrator tokens, and protect ~/.openclaw/credentials/homeassistant.json with strict filesystem permissions.

Risk: The documented Home Assistant setup permits plain HTTP, which can expose the token on untrusted networks.

Mitigation: Prefer an HTTPS Home Assistant URL and run commands only from trusted hosts and networks.

Risk: Write commands can change real lights, switches, and climate devices without built-in safeguards.

Mitigation: Review the target entity and requested action before execution, especially for thermostat mode, temperature, switch, and light control commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ricanwarfare/skills/ha-skill)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Home Assistant Climate Integration](https://www.home-assistant.io/integrations/climate/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, a reachable Home Assistant instance, and a local long-lived access token configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
