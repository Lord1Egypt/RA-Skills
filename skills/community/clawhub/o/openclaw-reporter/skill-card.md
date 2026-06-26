## Description: <br>
Opt-in reporter for the OpenClaw global claw heatmap that sends consent-gated heartbeats and manual task or token reports through the claw-market CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardwei195](https://clawhub.ai/user/richardwei195) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to opt in to OpenClaw activity reporting, register a chosen display name, and manually report completed work or token usage to the OpenClaw service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends platform, model, user-chosen claw name, generic task activity, IP-derived approximate location, and optional token counts to the OpenClaw service. <br>
Mitigation: Install and use it only after confirming that this telemetry is acceptable; first-time registration and optional token reporting require explicit consent. <br>
Risk: Registration stores a server-issued API key locally in ~/.openclaw/config.json. <br>
Mitigation: Keep the config file private, rely on the documented owner-only permissions, and run claw-market config clear to stop reporting and remove local credentials. <br>
Risk: The skill depends on the third-party @ricardweii/claw-market npm package and sends requests through that CLI. <br>
Mitigation: Verify that the package and publisher are trusted before installing it globally. <br>


## Reference(s): <br>
- [OpenClaw Reporter on ClawHub](https://clawhub.ai/richardwei195/openclaw-reporter) <br>
- [OpenClaw service endpoint](https://kymr.top/) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user consent before registration or optional token reporting; uses the claw-market CLI and stores configuration in ~/.openclaw/config.json.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
