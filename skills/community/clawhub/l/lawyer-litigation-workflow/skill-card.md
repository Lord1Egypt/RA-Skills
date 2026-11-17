## Description:

Automates a Chinese civil-litigation workflow for case intake, IRAC-style legal analysis, litigation document generation, comparable-case and statute retrieval, strategy review, and quality-control gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxiaole123](https://clawhub.ai/user/maxiaole123)

### License/Terms of Use:

AGPL-3.0

## Use Case:

External legal professionals use this skill to structure Chinese civil-litigation case intake, generate common litigation materials, organize evidence and case data, and review outputs through document QC and human confirmation pauses.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles confidential case data with broad local write authority and weak path/privacy controls.

Mitigation: Review before installing, run first with non-sensitive test data on a trusted machine, and keep privileged evidence out of shared or synced folders unless that sharing is intentional.

Risk: Case names containing slashes, absolute paths, or '..' can create path-handling risk.

Mitigation: Use simple case names without path separators, absolute path prefixes, or parent-directory segments.

Risk: The workflow creates persistent ~/.lawyer_workflow files and local trial/license tracking.

Mitigation: Review the local workspace and license files after use and remove data that should not remain on the machine.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maxiaole123/skills/lawyer-litigation-workflow)
- [律师诉讼自动化工作流 - 使用指南](references/000_使用指南_必读.md)
- [诉讼自动化工作流 SOP](references/001_SOP_全流程说明.md)
- [规格驱动管道说明](references/002_规格驱动管道.md)
- [IRAC 推理框架](references/003_IRAC推理框架.md)
- [模板映射表](references/004_模板映射表.md)
- [QC 质量门控说明](references/005_QC质量门控.md)
- [执业纪律铁律](references/006_执业纪律铁律.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated local case files, including DOCX documents, JSON case data, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and uses a persistent local workspace under ~/.lawyer_workflow and per-case output directories.]

## Skill Version(s):

1.0.2 (source: server release metadata and manifest.yaml; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
