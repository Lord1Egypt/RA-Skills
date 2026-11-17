## Description:

Sensor edition of iaiops — connect one industrial sensor and read it correctly: draft a sensor profile from a vendor IODD, check it, read one channel once with its unit, accuracy band and verification level, then collect. Covers sensors on Modbus RTU/TCP (RS-485 / RS-232 / RS-422 / USB serial, 4–20 mA via I/O modules), IO-Link masters (JSON interface) and MQTT/Sparkplug nodes. Use when the task mentions a sensor, sensor profile, IODD, IO-Link device, process data / pdin, decoding registers into engineering units, float32 word order, sentinel / no-target values, Modbus RTU instruments (RS-485 / RS-232), or "接一个传感器 / 传感器描述 / 读不懂寄存器 / 单位". The sensor tools are read-only and never write config; the server also exposes mqtt_publish (HIGH, MOC-gated) via the MQTT/Sparkplug set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and industrial engineers use the skill to draft and check sensor profiles, read a channel with its unit and verification level, and collect sensor data over supported industrial protocols. Profile binding and confirmation of device-specific details remain with the operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad “unit” trigger may activate the skill for unrelated requests.

Mitigation: Check that the request concerns sensor work before using the skill, and narrow the trigger if unrelated activations occur.

Risk: The MQTT/Sparkplug server set also exposes mqtt_publish, a high-risk device write.

Mitigation: Use this write only when explicitly required and follow its documented dry-run and management-of-change approval gate.

## Reference(s):

- [Industrial-AIOps Sensor on ClawHub](https://clawhub.ai/zw008/skills/iaiops-sensor)
- [Publisher profile (zw008)](https://clawhub.ai/user/zw008)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Text and Markdown with configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report channel values with units, accuracy bands, reachability and decodability status, and profile verification levels.]

## Skill Version(s):

0.34.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
