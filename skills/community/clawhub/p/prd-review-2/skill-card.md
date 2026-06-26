## Description: <br>
PRD 内审 Skill，对齐《PRD 文档标准规范 v2.4》。支持从飞书文档自动读取内容，识别 A/B/C 类型，按分型检查清单逐项审核，输出评分+必填项校验+逻辑校验+补全建议的结构化评审报告。触发关键词：审核、审查、检查、评审、内审、review、帮我审、PRD。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adahuhu](https://clawhub.ai/user/adahuhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and product operations teams use this skill to review PRD documents against a structured internal standard, classify the PRD type, and generate scoring, required-field checks, logic checks, and improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds Feishu app credentials in its artifact. <br>
Mitigation: Remove and rotate the embedded credentials before use, and provide credentials through an approved secret-management mechanism. <br>
Risk: The skill can read Feishu links, write reports back, save audit history, and reuse prior records. <br>
Mitigation: Use it only with documents the user is authorized to process, and require explicit confirmation before reading external documents, writing reports, saving audit history, or reusing prior records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adahuhu/prd-review-2) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Files] <br>
**Output Format:** [Structured Markdown review report with scoring, validation tables, logic checks, and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read Feishu documents, local files, or pasted text when authorized; may write review reports and audit history when confirmed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
