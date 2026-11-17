## Description:

帮助用户审计、共创、分阶段落地并持续优化基于 OpenClaw 的 GTD 个人知识管理（PKM）系统，适用于从零搭建、旧库重构、目录与标签策略、AGENTS.md/HEARTBEAT.md/TODO 自动化设计，以及后续迭代。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaor1995](https://clawhub.ai/user/zhaor1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to audit, design, phase in, and maintain a GTD-based personal knowledge management system for OpenClaw, Markdown, Obsidian, or local knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation recipes may read or persist chat history, memory files, TODO entries, project notes, and configuration data without sufficient privacy controls.

Mitigation: Before enabling HEARTBEAT, cron, log generation, memory cleanup, or configuration backups, define allowed input paths, output paths, access controls, and redaction or deletion rules.

Risk: Helper scripts can inspect or write files under the user-selected knowledge-base root, including generated reports, directories, templates, and starter documentation.

Mitigation: Run audit before restructuring, confirm the target root, keep a Git snapshot or backup before bulk changes, and use overwrite options only when replacement is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaor1995/skills/gtd-pkm)
- [Collaborative Design Playbook](references/collaborative-design-playbook.md)
- [GTD Knowledge Framework](references/gtd-knowledge-framework.md)
- [OpenClaw Automation Recipes](references/openclaw-automation-recipes.md)
- [OpenClaw Portable Patterns](references/openclaw-portable-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands, Python-script usage, and generated knowledge-base files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate audit reports, directory skeletons, templates, and configuration guidance only after the user selects a knowledge root and confirms the rollout stage.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
