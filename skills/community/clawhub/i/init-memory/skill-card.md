## Description: <br>
为任意项目初始化 Claude 持久化记忆系统（v3.0 搜索引擎模型）。自动扫描项目结构、技术栈、代码规范，生成完整的记忆文件和 CLAUDE.md 指令。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hplil](https://clawhub.ai/user/hplil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize project-specific Claude memory files after scanning a repository's structure, technology stack, conventions, modules, and existing Claude guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated memory files and CLAUDE.md may capture private project structure or conventions and influence future Claude sessions. <br>
Mitigation: Review the generated .claude/memory files and CLAUDE.md before committing them or relying on them. <br>
Risk: The --force option can replace existing generated memory content. <br>
Mitigation: Use --force only when the existing memory files are no longer needed or have been backed up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hplil/init-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON file templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local Claude memory files and CLAUDE.md guidance in the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
