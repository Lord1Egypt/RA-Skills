## Description:

九号电动车/平衡车集成技能 - 用于与 Ninebot 设备交互、诊断、配置和故障排除

This skill is ready for commercial/non-commercial use.

## Publisher:

[aninebot](https://clawhub.ai/user/aninebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and riders use this skill to interact with Ninebot scooters, balance vehicles, and e-bikes for connection, status checks, battery and ride data, configuration, diagnostics, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide changes to real Ninebot device settings, including speed limits, lights, resets, and firmware-related actions.

Mitigation: Require explicit user confirmation before applying configuration, reset, firmware, or speed-limit changes to a real vehicle.

Risk: Incorrect diagnostic or configuration guidance could affect vehicle behavior or user safety.

Mitigation: Review recommended actions before execution and avoid applying changes unless the device is stationary and sufficiently charged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aninebot/skills/ninebot-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Chinese-language commands and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ninebot device commands, status summaries, diagnostic guidance, and configuration recommendations.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
