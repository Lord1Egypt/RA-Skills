## Description:

从 iKuai 路由器的 ikuai-cli JSON 数据生成可视化 HTML 流量报表，包含总览、网络配置、流量分析、安全状态和系统日志视图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[veelove](https://clawhub.ai/user/veelove)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and technically proficient iKuai router owners use this skill to collect router telemetry with ikuai-cli and generate a browser-viewable traffic, configuration, security, and log report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report can expose router inventory, configuration, traffic details, and logs.

Mitigation: Treat the HTML output as confidential, store it in a private user-owned location, and redact sensitive values before sharing.

Risk: The skill relies on ikuai-cli authentication to collect router data.

Mitigation: Configure credentials only in trusted environments, review the ikuai-cli auth state before use, and rotate credentials if report output is exposed.

Risk: Router data is embedded into a local HTML report.

Mitigation: Review the generated file before routine use and add HTML escaping for dynamic values when adapting the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veelove/skills/ikuai-report)
- [ClawHub publisher profile](https://clawhub.ai/user/veelove)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration guidance]

**Output Format:** [Static HTML report file with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes /tmp/ikuai-report.html and requires ikuai-cli authentication to be configured.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
