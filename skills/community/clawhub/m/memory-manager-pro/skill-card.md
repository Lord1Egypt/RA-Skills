## Description:

Memory Manager Pro is an OpenClaw skill for three-level memory indexing, task tracking, keyword mapping, and tag-based retrieval across multiple projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guojiuben](https://clawhub.ai/user/guojiuben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create and maintain persistent project memory, task indexes, keyword maps, and tag-based retrieval structures for multi-project workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update persistent memory and project files across a workspace.

Mitigation: Use it in a dedicated workspace and review proposed file paths before allowing writes.

Risk: Other skills can call its index update interface, which may broaden write activity without enough scoping or confirmation.

Mitigation: Allow external-skill calls only from trusted skills and verify resolved paths remain inside intended memory and project folders.

Risk: Generic triggers may activate broad memory-management behavior unexpectedly.

Mitigation: Confirm the requested memory or task-management operation before executing changes.

## Reference(s):

- [Memory Manager Pro ClawHub page](https://clawhub.ai/guojiuben/skills/memory-manager-pro)
- [任务文件模板](references/任务模板.md)
- [关键词映射示例](references/关键词映射示例.md)
- [标签系统指南](references/标签系统指南.md)
- [目录结构标准](references/目录结构标准.md)
- [索引文件模板](references/索引模板.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, file paths, task templates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory and task-management structures; persistent file writes should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
