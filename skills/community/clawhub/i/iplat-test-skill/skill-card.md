## Description:

京东国际物流数据查询技能，支持物流轨迹追踪、国际供应链运营指标查询和跨境小包体验指标查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdl-external-skills](https://clawhub.ai/user/jdl-external-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and logistics operations teams use this skill to query JD international shipment tracking details and compare supply-chain or cross-border package KPI data by date, warehouse, continent, customer, and related dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends tokens plus shipment identifiers and business metrics to external JD/Ochama services.

Mitigation: Use only a scoped, revocable JD/Ochama token, disclose the external data transfer, and run the skill in a restricted environment.

Risk: The security evidence reports disabled TLS certificate checks in the helper scripts.

Mitigation: Remove rejectUnauthorized:false before production use and require normal certificate validation.

Risk: The security evidence reports shell command construction from user input without safe argument handling.

Mitigation: Validate command arguments and pass them through a non-shell API or equivalent safe execution boundary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdl-external-skills/skills/iplat-test-skill)
- [README.md](README.md)
- [Logistics tracking skill documentation](skills/joy-logistics-trace/SKILL.md)
- [Supply-chain KPI skill documentation](skills/joy-logistics-indicator/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell command examples and JSON API response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include command invocations for Node.js helper scripts and summarized logistics or KPI results returned by external JD/Ochama services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
