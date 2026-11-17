## Description:

PRD 内审 Skill，对齐《PRD 文档标准规范 v2.4》。支持从飞书文档自动读取内容，识别 A/B/C 类型，按分型检查清单逐项审核，输出评分+必填项校验+逻辑校验+补全建议的结构化评审报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[adahuhu](https://clawhub.ai/user/adahuhu)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and product operations teams use this skill to review PRDs for cross-border e-commerce SaaS systems such as ERP, SCM, WMS, and LPS. It classifies PRDs into A, B, or C types, checks required structure and logic, scores quality, and suggests concrete improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release contains a plaintext Feishu app secret.

Mitigation: Remove the secret, rotate it before any installation, and require user-scoped Feishu authorization before document access.

Risk: Review history may contain sensitive PRD content or review findings.

Mitigation: Make audit-history storage opt-in and document retention, access, and deletion controls before use.

Risk: Optional Feishu write-back could publish review reports to the wrong audience.

Mitigation: Require explicit confirmation before write-back and verify document permissions after import.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adahuhu/skills/prd-review-2)
- [ClawHub publisher profile](https://clawhub.ai/user/adahuhu)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Structured Markdown review reports with optional JSON audit-history records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include PRD type classification, required-item checks, scoring, issue lists, logic checks, improvement guidance, and optional re-review comparison.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
