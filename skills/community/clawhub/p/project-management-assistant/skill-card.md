## Description:

项目管理助手（PM Assistant）协助项目经理、交付人员、客户经理、PMO和管理层完成项目启动信息提取、WBS任务分解、进度整理、风险预警、周报生成、客户沟通跟踪、交付物验收归档与项目复盘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, delivery teams, account managers, PMO staff, and management use this skill to structure project initiation, planning, progress tracking, risk review, weekly reporting, customer follow-up, delivery archiving, and retrospectives. It produces drafts, checklists, summaries, reminders, and review items while routing commitments, scope changes, sensitive data, and acceptance conclusions to human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-management documents can contain customer, employee, contract, financial, or non-public technical information.

Mitigation: Configure Feishu bot permissions, Hermes skill access, knowledge-base retrieval, audit logs, archive locations, retention periods, and sensitive-data redaction for only the relevant projects and users.

Risk: Generated project outputs could be mistaken for final commitments, scope changes, delay decisions, customer responses, or acceptance conclusions.

Mitigation: Require responsible human confirmation before external commitments, contract-scope changes, formal customer replies, delay decisions, or final acceptance conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeicn/skills/project-management-assistant)
- [README](artifact/README.md)
- [Workflows](artifact/workflows.md)
- [Runbook](artifact/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Structured Markdown and text using project-management templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes project charters, WBS tables, milestone plans, progress summaries, risk registers, weekly reports, customer reply suggestions, archive indexes, retrospectives, and human-confirmation items.]

## Skill Version(s):

0.1.0 (source: evidence.release.version, artifact/README.md, artifact/employee.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
