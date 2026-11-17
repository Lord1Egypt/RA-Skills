## Description:

DG-LAB is an OpenClaw plugin that connects to DG-Lab Coyote V3 electrostimulation devices over WebSocket and exposes chat commands, agent tools, QR pairing, waveform playback, and optional emotion-triggered stimulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengying1314](https://clawhub.ai/user/fengying1314)

### License/Terms of Use:

MIT

## Use Case:

External users and OpenClaw developers use this plugin to pair DG-Lab Coyote V3 hardware with an OpenClaw gateway, manage device status and limits, and allow an agent to send controlled stimulation or waveform commands. It is intended for supervised environments where the operator understands the physical-device risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent or emotion-triggered commands can cause unsafe physical stimulation.

Mitigation: Require explicit human confirmation outside the plugin before stimulation, keep emotion mode disabled unless deliberately supervised, start from the lowest intensity, and set conservative hardware limits in the DG-Lab app.

Risk: The WebSocket service can expose physical-device control if reachable from untrusted networks.

Mitigation: Run only in a tightly controlled environment, avoid exposing the WebSocket port directly to the Internet, and restrict network access around the configured port.

Risk: The one-click curl-to-bash installation path increases install-time review risk.

Mitigation: Prefer the OpenClaw or npm package installation path and review the package before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengying1314/skills/openclaw-plugin-dg-lab-skill)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [DG-Lab V3 Socket Control Protocol](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/README.md)
- [DG-Lab V3 frequency compression algorithm](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/coyote/extra/README.md)
- [npm package](https://www.npmjs.com/package/openclaw-plugin-dg-lab)

## Skill Output:

**Output Type(s):** [text, API calls, shell commands, configuration, guidance]

**Output Format:** [OpenClaw chat commands, agent tool calls, status text, QR-code file paths, JSON-style configuration, and Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls a physical device through a local OpenClaw plugin and WebSocket pairing flow; outputs should be reviewed before enabling agent-triggered stimulation.]

## Skill Version(s):

1.0.3 (source: evidence release metadata, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
