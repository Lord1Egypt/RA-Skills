## Description: <br>
Obsidian CLI工具免费版帮助AI Agent通过命令行操作本地Obsidian笔记库，用于创建、读取、搜索和基础管理笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal knowledge-management users use this skill to let an agent operate an Obsidian vault from the command line for note creation, reading, search, tag lookup, daily notes, basic task handling, and frontmatter property updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to create notes, append content, edit frontmatter properties, or toggle tasks in a local Obsidian vault. <br>
Mitigation: Require explicit confirmation before vault-modifying commands, especially in a primary vault without backups or version control. <br>
Risk: The skill reads and searches local vault content, which may include private notes. <br>
Mitigation: Use the skill only for explicit Obsidian tasks and only on vaults whose contents the user intends the agent to access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/obsidian-cli-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Obsidian application and obsidian CLI; commands may read or modify vault files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
