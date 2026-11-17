## Description:

为任意项目初始化 Claude 持久化记忆系统（v3.0 搜索引擎模型）。自动扫描项目结构、技术栈、代码规范，生成完整的记忆文件和 CLAUDE.md 指令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hplil](https://clawhub.ai/user/hplil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize a project-local Claude memory system that captures architecture, conventions, semantic indexes, changelog state, and related guidance. It is intended for projects that want persistent agent context stored in .claude/memory and referenced from CLAUDE.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated memory files may summarize internal architecture, conventions, bug history, and other project details.

Mitigation: Review .claude/memory files and CLAUDE.md before committing, sharing, or deploying the generated content.

Risk: The skill intentionally writes project-local memory files and adds Claude-specific instructions to CLAUDE.md.

Mitigation: Install it only in projects where those persistent files and instructions are desired, and use the documented --force behavior carefully when replacing existing memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hplil/skills/init-memory)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown and JSON files with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports --force, --minimal, --lang zh, and --lang en; writes project-local .claude/memory files and CLAUDE.md instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
