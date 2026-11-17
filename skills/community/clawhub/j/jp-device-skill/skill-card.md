## Description:

jp-device-skill is a Chinese-language placeholder skill for JinPeng smart tricycle vehicle queries that currently returns a fixed testing response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyang-1](https://clawhub.ai/user/zhangyang-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents can route JinPeng smart tricycle vehicle status, battery, mileage, trip, location, parameter, and troubleshooting queries to this skill. This release currently provides a testing placeholder response rather than live vehicle integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect real-time JinPeng vehicle data or control even though this release is only a placeholder.

Mitigation: Treat the response as a testing notice until a later release provides verified live vehicle integration.

Risk: A future vehicle-connected version could involve sensitive location, trip, or vehicle-setting data.

Mitigation: Require explicit permission before accessing location or trip data and confirm setting changes such as speed limits before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyang-1/skills/jp-device-skill)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Currently returns the fixed Chinese testing notice: 该skill正在测试中，敬请期待。]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
