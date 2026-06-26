## Description: <br>
DG-LAB connects OpenClaw agents to DG-Lab Coyote V3 e-stim devices over WebSocket for QR pairing, command-driven stimulation, pulse management, and emotion-triggered stimulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengying1314](https://clawhub.ai/user/fengying1314) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and OpenClaw developers use this plugin to pair a DG-Lab V3 device, expose chat commands and agent tools for stimulation control, and manage waveform presets. It should be used only for deliberate, supervised physical-device operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI tools and keyword-based emotion hooks can trigger physical stimulation without a clear per-action confirmation step. <br>
Mitigation: Keep emotion mode disabled unless actively monitored, require deliberate tool use for stimulation, and set conservative hardware limits in the DG-Lab app before enabling the plugin. <br>
Risk: Misuse of an e-stim device can cause physical harm. <br>
Mitigation: Use only with informed adult supervision, start at the lowest intensity, avoid unsafe body locations and medical contraindications, and follow DG-Lab safety guidance. <br>
Risk: The WebSocket service, QR pairing content, or control links could expose device control to untrusted parties. <br>
Mitigation: Bind or firewall the configured port to trusted networks, avoid sharing QR or control links, and rotate pairing sessions if exposure is suspected. <br>
Risk: Software intensity limits are convenience controls rather than a safety guarantee. <br>
Mitigation: Set low device-side hardware limits, monitor reported strength and limit feedback, and treat software clamping as secondary protection only. <br>
Risk: The remote shell installer increases installation-chain risk. <br>
Mitigation: Prefer the OpenClaw or NPM install path, and review installation scripts before running them in a shell. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/fengying1314/openclaw-plugin-dg-lab-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fengying1314) <br>
- [NPM package: openclaw-plugin-dg-lab](https://www.npmjs.com/package/openclaw-plugin-dg-lab) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [DG-Lab V3 Socket Control Protocol](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/README.md) <br>
- [DG-Lab V3 frequency compression algorithm](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/coyote/extra/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and text responses with JSON configuration snippets, shell commands, and generated QR code image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can issue WebSocket commands to a connected physical device and can return status, waveform lists, and pairing QR file paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.json release.version, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
