## Description:

办公效率技能库：覆盖 Office/PDF 与 Markdown 双向转换、专业演示设计与 PPT 编程自动化四大能力，并附文档样式与演示大纲的确定性检查脚本；另提供办公品牌与模板上下文记忆，让多次产出保持统一版式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

开发者和小团队可用此技能在 Office、PDF 与 Markdown 之间转换文档，设计和自动化 PowerPoint 演示，并复用品牌模板偏好及检查交付稿件的结构。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples use global, auto-confirming commands.

Mitigation: Review installation commands and dependency versions before running them.

Risk: Document conversion may affect source fidelity.

Mitigation: Retain source copies during conversion.

Risk: Optional Vision or MCP services may handle confidential documents.

Mitigation: Review those services separately before using them with confidential documents; their implementations are not bundled.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/skills-repo/skills/office-master)
- [Office and Markdown conversion guide](references/office-md-roundtrip.md)
- [Presentation design system](references/presentation-design-system.md)
- [Document style quality gates](references/doc-style-quality-gates.md)
- [Office context playbook](references/office-context-playbook.md)
- [office-to-md source skill](https://skills.sh/claude-office-skills/skills/office-to-md)
- [md-to-office source skill](https://skills.sh/claude-office-skills/skills/md-to-office)
- [presentation-designer source skill](https://skills.sh/willem4130/claude-code-skills/elite-powerpoint-designer)
- [ppt-automation source skill](https://skills.sh/practicalswan/agent-skills/powerpoint-ppt)

## Skill Output:

**Output Type(s):** [Markdown, Office documents, PDF, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, Office/PDF files, and scripts; varies by task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File outputs depend on the selected conversion, document-checking, or presentation workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
