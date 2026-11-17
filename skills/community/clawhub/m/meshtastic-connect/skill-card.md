## Description:

Connect an OpenClaw gateway to a Meshtastic LoRa mesh node in minutes — install the maintained channel plugin (@fintlp/openclaw-meshtastic), run the probe-first setup wizard, and verify the first DM over radio. Use when a user wants their AI agent reachable via Meshtastic, off-grid messaging, or LoRa mesh comms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fintlp](https://clawhub.ai/user/fintlp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and radio operators use this skill to connect an OpenClaw agent to a reachable Meshtastic node for off-grid messaging, configure access controls, and verify radio DMs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because a referenced local path could not be resolved, so its evidence is incomplete.

Mitigation: Review the missing reference and confirm any dependent guidance before installation.

Risk: Node maps can expose other people's real-world radio locations, and sharing a map link exposes its contents to the viewer and can persist the link in chat or browser history.

Mitigation: Prefer a local offline map, keep coordinate files private, and create an external viewer link only on explicit owner request with the exposure explained.

Risk: Group radio transmissions use shared airtime and cannot be recalled once sent.

Mitigation: Keep group transmission disabled unless the owner deliberately enables it; retain pairing or allowlist access controls for DMs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fintlp/skills/meshtastic-connect)
- [Meshtastic plugin issue tracker](https://github.com/fintlp/openclaw-meshtastic/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, GeoJSON]

**Output Format:** [Markdown guidance with shell commands and optional GeoJSON map instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional node maps can contain real-world radio coordinates.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
