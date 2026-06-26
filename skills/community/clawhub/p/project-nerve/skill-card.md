## Description: <br>
项目中枢 — 跨平台项目管理聚合器，统一管理 Trello、GitHub Issues、Linear、Notion、Obsidian 任务，支持自学习引擎和任务关系图谱 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project leads, and team operators use this skill to connect project-management sources, aggregate and search tasks, create or update work items, generate standup and sprint reports, and inspect task dependencies across supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured project-management credentials may allow reading or modifying tasks across connected services. <br>
Mitigation: Use least-privilege tokens, configure only required services, and confirm the target platform before creating or updating important tasks. <br>
Risk: Local cache, learning, or graph data may contain sensitive project information. <br>
Mitigation: Point Obsidian at a task-specific vault or folder when possible and periodically reset local learning/cache data if it may contain sensitive information. <br>


## Reference(s): <br>
- [Project Nerve on ClawHub](https://clawhub.ai/hanjing5024064/project-nerve) <br>
- [API Guide](references/api-guide.md) <br>
- [Unified Task Schema](references/unified-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, summaries, inline shell commands, JSON command payloads, and Mermaid diagrams when supported] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local cache, configuration, learning, and task graph files while using configured project-management credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
