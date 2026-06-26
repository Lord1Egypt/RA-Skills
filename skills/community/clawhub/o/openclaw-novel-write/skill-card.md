## Description: <br>
OpenClaw 小说创作 Skill - 基于七步方法论的 AI 辅助写作系统 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martin-yyds](https://clawhub.ai/user/martin-yyds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers and OpenClaw users use this skill to plan, track, draft, revise, and analyze Chinese fiction projects through a structured novel-writing workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad conversational triggers may start project setup, writing, tracking, or cleanup steps when the user intended only discussion. <br>
Mitigation: Use explicit /novel commands for important actions and confirm the requested operation before allowing file changes. <br>
Risk: The skill can create and update many project files, including drafts, tracking JSON, timelines, task lists, and knowledge-base copies. <br>
Mitigation: Run it in a dedicated writing workspace and keep backups or version control before major workflow steps. <br>
Risk: Initialization can target a user-provided path, which may place generated files outside the intended project area. <br>
Mitigation: Check the resolved target path before initialization and avoid running the skill from sensitive directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/martin-yyds/openclaw-novel-write) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/martin-yyds) <br>
- [README](README.md) <br>
- [Writing command reference](commands/write.md) <br>
- [Requirements knowledge base](knowledge-base/requirements/README.md) <br>
- [Styles knowledge base](knowledge-base/styles/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON tracking files, shell command snippets, and project file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates novel project files, tracking JSON, writing knowledge-base copies, chapter drafts, analysis reports, timelines, diagrams, and task lists.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
