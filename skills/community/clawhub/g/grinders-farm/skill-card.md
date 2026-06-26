## Description: <br>
Requires grinders-farm CLI + openclaw-plugin-grinders-farm before use. Maps intents to grinders_farm. 使用前需先安装 grinders-farm 与 openclaw-plugin-grinders-farm。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visawang](https://clawhub.ai/user/visawang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to convert farm-game chat intents into a single grinders_farm command for planting, watering, harvesting, selling, viewing inventory, and controlling auto-advance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented plugin install uses an unsafe OpenClaw install path. <br>
Mitigation: Install only after reviewing the publisher and plugin package, and keep the OpenClaw Gateway restart and plugin inspection steps explicit. <br>
Risk: Auto-advance can run as a local background worker and post updates to bound chat channels. <br>
Mitigation: Review channel bindings before starting auto-advance, use /farm stop when not needed, and consider setting autoStartWorkerOnGatewayBoot to false. <br>
Risk: The skill and plugin persist farm state and chat-routing files under ~/.grinders-farm. <br>
Mitigation: Review the local files before sharing a machine or channel configuration, especially openclaw-deliveries.json. <br>
Risk: The reset command starts a new game and can erase the current farm state. <br>
Mitigation: Avoid reset unless the user clearly intends to discard the current farm. <br>
Risk: The artifact includes start.sh with unrelated Docker/GPU scheduler behavior. <br>
Mitigation: Do not run start.sh unless it has been independently audited and is needed for a separate purpose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/visawang/grinders-farm) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [OpenClaw plugin README](openclaw-plugin/README.md) <br>
- [OpenClaw plugin manifest](openclaw-plugin/openclaw.plugin.json) <br>
- [Farm preview image](docs/images/demo-farm.png) <br>


## Skill Output: <br>
**Output Type(s):** [Tool calls, Text, Markdown, Links, Guidance] <br>
**Output Format:** [Markdown or plain text from the grinders_farm tool, with markdown tables preserved and image URLs kept as clickable links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maps each supported farm intent to exactly one grinders_farm command; failures should return the error first and one executable example command.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
