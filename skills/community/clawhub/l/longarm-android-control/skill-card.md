## Description:

Longarm Control helps agents drive an Android device running longarm through its HTTP API or MCP server for gestures, screenshots, app and intent launch, overlay controls, and batch automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metaphorproj](https://clawhub.ai/user/metaphorproj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to longarm and control a reachable Android device for UI navigation, screenshots, app launching, and repeatable batch tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext remote control can expose bearer tokens or device actions on an untrusted network.

Mitigation: Use the skill only with a trusted longarm device/server over a trusted network or encrypted tunnel, avoid sending tokens over plaintext HTTP, and enable authentication.

Risk: Screenshots and exported batch history can contain sensitive device content.

Mitigation: Treat screenshots and exports as sensitive data, store or share them only where appropriate, and delete unneeded history artifacts.

Risk: Remote gestures, app launches, intent opens, and batch tasks can change device state.

Mitigation: Confirm destructive or device-changing actions before letting an agent run them.

## Reference(s):

- [longarm HTTP API Reference](references/api.md)
- [longarm MCP Reference](references/mcp.md)
- [Server-resolved GitHub provenance](https://github.com/metaphorproj/longarm-skills/tree/main/skills/longarm-android-control)
- [ClawHub skill page](https://clawhub.ai/metaphorproj/skills/longarm-android-control)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, and optional generated image or archive files from longarm endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include PNG screenshots and ZIP exports when the agent uses longarm history or screenshot commands.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
