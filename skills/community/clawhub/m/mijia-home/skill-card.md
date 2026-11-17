## Description:

小米/米家智能家居控制帮助代理查询和控制连接的小米/米家灯具、空气净化器、空调、风扇、扫地机器人、窗帘和摄像头等设备。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alleneee](https://clawhub.ai/user/alleneee)

### License/Terms of Use:

MIT-0

## Use Case:

Smart-home users use this skill to let an agent operate Xiaomi/Mijia home devices, check device status, run multi-device scenes, and capture camera snapshots. It should be used only with a trusted xiaomi-home MCP server and with explicit confirmation for sensitive physical or camera actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide Xiaomi passwords or verification codes in chat.

Mitigation: Use only a trusted MCP server, review where credentials are stored or logged, and avoid entering passwords or verification codes unless that handling is acceptable.

Risk: The skill can trigger broad physical actions across smart-home devices, including scenes, bulk changes, heaters, climate devices, and cameras.

Mitigation: Require explicit user confirmation before scenes, bulk device changes, heater or climate changes, camera snapshots, or RTSP camera setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alleneee/skills/mijia-home)
- [ClawHub publisher profile](https://clawhub.ai/user/alleneee)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Natural language responses with structured MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request Xiaomi account credentials, verification codes, device identifiers, camera names, or RTSP URLs when required by the configured MCP server.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
