## Description:

Controls Xiaomi and Xiao AI smart-home devices through the Home Assistant API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipluuup](https://clawhub.ai/user/pipluuup)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to turn Xiaomi device requests into Home Assistant service calls for configured speakers, air conditioners, lights, and other entities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue authenticated Home Assistant commands that affect physical smart-home devices.

Mitigation: Use a dedicated least-privileged Home Assistant token, restrict allowed entities and actions, and require confirmation for speaker, HVAC, lock, alarm, or other physical-device commands.

Risk: The default Home Assistant URL uses HTTP on a local network.

Mitigation: Prefer HTTPS for Home Assistant access, including remote or shared-network deployments.

Risk: Broad or weakly scoped entity control can trigger unintended device actions.

Mitigation: Limit the skill to known entity IDs and reviewed service calls before enabling it for an agent.

## Reference(s):

- [Home Assistant Entity Reference](references/entities.md)
- [ClawHub Skill Page](https://clawhub.ai/pipluuup/skills/haxiaomicontrol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Home Assistant API examples and optional Python command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated Home Assistant service calls for user-configured smart-home entities.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
