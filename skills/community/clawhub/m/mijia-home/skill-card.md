## Description: <br>
Controls Xiaomi/Mijia smart-home devices through a trusted xiaomi-home MCP server, including lights, purifiers, heaters, air conditioners, fans, vacuums, curtains, status queries, and camera snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alleneee](https://clawhub.ai/user/alleneee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Xiaomi/Mijia smart-home devices use this skill to let an agent authenticate with the xiaomi-home MCP server, locate devices from natural-language requests, read status, control device properties or actions, and analyze camera snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide Xiaomi account credentials during setup. <br>
Mitigation: Install only with a trusted xiaomi-home MCP server and use platform secret handling instead of exposing credentials in chat whenever available. <br>
Risk: The skill can control cameras and multiple smart-home devices, including heaters, air conditioners, scenes, and other household equipment. <br>
Mitigation: Require explicit user confirmation before camera access, bulk scene execution, heater or AC changes, or any action affecting multiple devices. <br>
Risk: Device property IDs vary by model, so an incorrect action could fail or change the wrong property. <br>
Mitigation: Resolve devices with list or find tools, verify online status, and read or probe supported properties before changing device state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alleneee/mijia-home) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Natural-language responses with MCP tool calls and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may trigger authentication, smart-home device control, scene operations, or camera snapshots through the configured MCP server.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
