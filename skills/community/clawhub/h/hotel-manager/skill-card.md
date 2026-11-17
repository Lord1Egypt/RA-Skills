## Description:

酒店管家 Skill - 管理酒店 OTA 基础信息、房价库存及订单同步。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolful](https://clawhub.ai/user/wolful)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel operators and agents use this skill to coordinate OTA hotel information, room pricing, inventory controls, and order synchronization across API and browser automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live OTA prices, inventory, and orders using broad credentials.

Mitigation: Use sandbox or test credentials first, restrict OTA/PMS keys to the minimum required permissions, and require explicit human approval before saves, bulk price updates, inventory changes, or continuous order sync.

Risk: Browser automation can submit changes through OTA web consoles.

Mitigation: Require screenshots or logs after each change and verify the target platform, room type, date, and submitted value before committing updates.

Risk: Credential-backed integrations may reach unintended endpoints if configuration is changed.

Mitigation: Lock endpoints to trusted OTA and PMS hosts and review environment variables or config files before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wolful/skills/hotel-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript scripts, JSON configuration examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls or browser actions that update live OTA prices, inventory, and order data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
