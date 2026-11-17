## Description:

Use the oo CLI to inspect MQTT action schemas, receive messages, and publish messages through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect the MQTT connector's live action schemas, receive messages, and publish messages through an OOMOL-connected account. Publishing changes MQTT state and requires confirmation of the exact payload and effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute changing third-party installation code, and the bundled instructions do not establish the installer's exact effects.

Mitigation: Review the CLI installation separately; use a reviewed, version-pinned release with verified integrity, and check its automatic agent-skill synchronization settings.

Risk: Publishing sends a message to an MQTT destination and can change external state.

Mitigation: Confirm the destination topic, payload, and effect before publishing.

## Reference(s):

- [MQTT](https://mqtt.org)
- [MQTT specification](https://mqtt.org/mqtt-specification/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [MQTT ClawHub release](https://clawhub.ai/oomol/skills/oo-mqtt)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and action responses, plus Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
