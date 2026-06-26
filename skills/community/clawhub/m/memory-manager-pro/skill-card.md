## Description: <br>
Memory Manager Pro helps OpenClaw agents organize project memory and tasks through a three-level Markdown index, task tracking, keyword mapping, and tag-based retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guojiuben](https://clawhub.ai/user/guojiuben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, researchers, and OpenClaw users use this skill to create and maintain local Markdown memory indexes, task records, keyword maps, and project navigation files across multiple projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local memory and task files in the workspace. <br>
Mitigation: Install it only in workspaces where the agent is expected to maintain those files, and keep backups for important project files. <br>
Risk: Bulk or cross-skill index updates can route work through incorrect keyword mappings. <br>
Mitigation: Review keyword mappings before broad updates or external skill calls. <br>
Risk: Memory and task records may accidentally contain sensitive information. <br>
Mitigation: Avoid storing secrets in memory, task, keyword, or project records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guojiuben/memory-manager-pro) <br>
- [README](README.md) <br>
- [Directory structure standard](references/目录结构标准.md) <br>
- [Task templates](references/任务模板.md) <br>
- [Index templates](references/索引模板.md) <br>
- [Keyword mapping examples](references/关键词映射示例.md) <br>
- [Tag system guide](references/标签系统指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-like request examples, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local workspace memory, task, keyword, tag, and index files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and README changelog, released 2026-04-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
