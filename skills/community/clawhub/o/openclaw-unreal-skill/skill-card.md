## Description: <br>
Connects OpenClaw agents to Unreal Engine 5.x Editor so they can inspect and automate levels, actors, transforms, editor state, debug data, input, assets, console commands, and blueprints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TomLeeLive](https://clawhub.ai/user/TomLeeLive) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and Unreal Engine users use this skill to connect OpenClaw to Unreal Editor and automate editor workflows such as scene inspection, actor creation, transform changes, play mode control, debugging, input simulation, asset operations, and console commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad AI-controlled changes into a live Unreal project. <br>
Mitigation: Use source control or backups, test in a separate project first, and require explicit approval for deletes, saves, imports, property changes, and other project-changing actions. <br>
Risk: Unauthenticated local HTTP endpoints and a generic command bridge may be exposed beyond the intended local development environment. <br>
Mitigation: Keep the gateway local and firewalled, avoid exposing the MCP port or Unreal endpoints to untrusted networks, and verify the separate Unreal plugin before use. <br>
Risk: The skill can request screenshots, logs, input simulation, and console command execution. <br>
Mitigation: Require explicit approval for screenshots, log access, input simulation, and console commands before executing them. <br>


## Reference(s): <br>
- [Skill documentation](SKILL.md) <br>
- [README](README.md) <br>
- [OpenClaw Unreal Plugin](https://github.com/openclaw/openclaw-unreal-plugin) <br>
- [ClawHub release page](https://clawhub.ai/TomLeeLive/openclaw-unreal-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON-formatted tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool results may include Unreal session status, command responses, logs, screenshots, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
