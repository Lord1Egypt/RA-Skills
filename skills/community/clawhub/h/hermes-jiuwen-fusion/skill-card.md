## Description: <br>
融合 Hermes Agent 与 JiuwenClaw 精华的自进化多Agent协作系统，为 OpenClaw 多Agent工作流提供闭环学习、技能沉淀、自纠错、上下文瘦身、分层记忆与事件驱动协同。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gray163](https://clawhub.ai/user/gray163) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run complex OpenClaw tasks through a PM-led multi-agent workflow with executor, supervisor, and QA roles. It also guides agents to capture reusable lessons, maintain project memory, and evolve skill definitions after higher-complexity work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to maintain long-term project memory and write generated skills, which may persist sensitive data or low-quality guidance. <br>
Mitigation: Require approval before memory or SKILL.md writes, prohibit storing secrets, and review diffs before keeping generated content. <br>
Risk: Automatic skill creation and self-correction can alter reusable agent behavior across future tasks. <br>
Mitigation: Scan and review generated or modified skills before deployment, and keep backups or a rollback path for skill-library changes. <br>
Risk: Context slimming can replace detailed history with summaries that omit important constraints. <br>
Mitigation: Keep summaries task-scoped and self-contained, and review critical decisions before passing summaries to other agents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gray163/hermes-jiuwen-fusion) <br>
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) <br>
- [JiuwenClaw](https://gitcode.com/openJiuwen/jiuwenclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to write project memory files and generated or modified SKILL.md files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
