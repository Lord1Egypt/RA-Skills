## Description: <br>
Multi Agent Dev guides agents through a multi-agent development workflow that routes simple tasks to OpenClaw, medium tasks to subagents, and complex iterative work to Ralph Loop with configurable coding executors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehe973781230](https://clawhub.ai/user/hehe973781230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to structure coding tasks, choose an execution path, and generate Ralph Loop prompts and commands for iterative code changes, testing, documentation updates, and skill refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-driven development workflows can run commands or create directories in a project. <br>
Mitigation: Specify the project directory and task explicitly, and review proposed command execution or directory creation before allowing changes. <br>
Risk: Generated development guidance or proposed code changes may be incorrect or too broad for the target project. <br>
Mitigation: Review generated plans, file changes, and test results before relying on the output or deploying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hehe973781230/skills/multi-agent-dev) <br>
- [Ralph Wiggum](https://github.com/Th0rgal/open-ralph-wiggum) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task templates, executor selection guidance, and completion markers for Ralph Loop workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
