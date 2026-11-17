## Description:

嘉为蓝鲸 ITSM 工单分析技能，支持多流程工单数据读取、字段智能映射、新工单处理建议、趋势分析、高频问题识别和 SLA 监控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaeljochen](https://clawhub.ai/user/michaeljochen)

### License/Terms of Use:

MIT-0

## Use Case:

ITSM operations teams and support engineers use this skill to analyze Jiawei BlueKing ITSM ticket exports, estimate workload, review response times, classify recurring issues, and generate daily or weekly reports. It can also produce handling suggestions for new tickets from historical CSV or Excel data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ITSM exports and generated reports may contain personal, account, incident, or internal system details.

Mitigation: Treat inputs and reports as confidential and redact unnecessary sensitive fields before analysis or sharing.

Risk: Optional webhook or scheduled report delivery can expose ticket details to unintended destinations.

Mitigation: Review the destination and report contents before enabling scheduled pushes or webhook sharing.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install in a dedicated virtual environment and prefer pinned versions or a reviewed lock file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaeljochen/skills/itsm-ticket-analyzer)
- [Publisher profile](https://clawhub.ai/user/michaeljochen)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and recommendations, optional JSON from analysis scripts, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local CSV or Excel ticket exports and may write report files when an output path is supplied.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
