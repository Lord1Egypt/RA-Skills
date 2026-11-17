## Description:

根据技术方案、交底书草稿、发明构思或既有报告，创建并迭代完善中文专利申请前预评估报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent, IP, and research administration teams use this skill to turn invention disclosures or technical concepts into Chinese patent pre-evaluation reports with novelty search strategy, prior-art comparison, patentability risk analysis, abnormal-application risk checks, and application strategy recommendations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Confidential invention details may be sent to external PatSnap MCP services during novelty searches.

Mitigation: Use the skill only when authorized to use the configured PatSnap services, obtain explicit approval before searching unpublished or trade-secret material, and redact sensitive details before external queries.

Risk: The generated report may include hardcoded China University of Mining and Technology or PatSnap branding and confidentiality language that does not match the user's actual authorization or data handling.

Mitigation: Confirm permission to create branded reports and verify that the final confidentiality statement accurately reflects what was transmitted, searched, modified, exported, and reviewed.

Risk: Patentability conclusions can be misleading if MCP search evidence is incomplete, unavailable, or unreviewed.

Mitigation: Require patent or IP staff review before relying on conclusions, and keep unsupported items marked as 待补充 or 待复核.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-pre-evaluation-report)
- [Report workflow reference](artifact/references/report-workflow.md)
- [PatSnap MCP marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap authentication guide](https://open.zhihuiya.com/devportal/guides/authentication)
- [PatSnap security center](https://www.zhihuiya.com/security-center)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Self-contained HTML report with structured tables, styled sections, and report attachments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report workflow requires real PatSnap/智慧芽 MCP search evidence when available and marks incomplete or unverified facts as 待补充 or 待复核.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
