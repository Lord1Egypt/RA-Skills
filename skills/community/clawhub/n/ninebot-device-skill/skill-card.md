## Description:

九号电动车(Ninebot)车辆信息查询，支持九号电动车、九号电动摩托车，提供车辆开关机状态、车辆充电状态、车辆位置、车辆剩余电量、车辆剩余里程、车辆剩余充电时间等数据的查询功能

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninebot-app](https://clawhub.ai/user/ninebot-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query Ninebot electric vehicle status, charging state, battery level, estimated range, remaining charging time, and location through the Ninebot Device Service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Ninebot Device Service API key and can access sensitive vehicle data, including location.

Mitigation: Install only where access to this data is acceptable, prefer NINEBOT_DEVICESERVICE_KEY for the key, and avoid putting real keys in config.json or command-line arguments.

Risk: Local configuration can redirect authenticated requests or expose the API key if run from an untrusted directory.

Mitigation: Run the skill from a trusted directory and review any config.json or custom config before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninebot-app/skills/ninebot-device-skill)
- [Ninebot API assumptions](references/api-spec.md)
- [Ninebot API gateway](https://cn-cbu-gateway.ninebot.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NINEBOT_DEVICESERVICE_KEY or an equivalent local API key configuration.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
