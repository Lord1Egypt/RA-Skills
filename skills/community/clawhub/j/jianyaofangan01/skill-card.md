## Description:

编写简要方案（IT 规划方案/工作方案）。当用户输入"简要方案##"或"简要方案"时触发。提供结构化协作式方案编写流程：背景讨论→现状分析→问题及需求梳理→方案规划→预算概要。最终通过 Python 脚本基于模板 .docx 生成 Word 文档。适用于政府/国企 IT 项目方案、网络安全规划、信息化建设方案等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomm1399](https://clawhub.ai/user/tomm1399)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, proposal writers, and IT planners use this skill to draft concise government or state-owned enterprise IT planning proposals through a staged workflow covering background, current-state analysis, prioritized needs, planning, budget summary, and Word document generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposal state may be saved locally in plaintext JSON files, which can expose sensitive project context, infrastructure details, or folder tokens.

Mitigation: Confirm the storage location before use, avoid saving credentials or sensitive infrastructure details, and delete proposal state files after completion.

Risk: Generated documents may be uploaded to Feishu cloud storage without detailed scoping or retention guidance.

Mitigation: Use approved cloud folders, verify sharing permissions before upload, and remove sensitive personal, cost, or competitive information during human review.

Risk: The workflow depends on Python document generation with python-docx.

Mitigation: Use a pinned dependency setup and review generated Word formatting before distribution.

## Reference(s):

- [简要方案模板参考](artifact/references/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Python code and Word document workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON proposal state files and generated .docx proposal documents when used by an agent with filesystem and document-generation tools.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
