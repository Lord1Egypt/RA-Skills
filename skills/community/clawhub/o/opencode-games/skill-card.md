## Description: <br>
Spawn OpenCode as an ACP (Agent Client Protocol) subagent for complex coding tasks, including games, web apps, multi-file projects, and production code generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jadegaul](https://clawhub.ai/user/jadegaul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate game, web app, multi-file project, refactoring, and bug-fix work to OpenCode through ACP. It is especially focused on HTML5 game creation and coding workflows that benefit from a dedicated coding agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate broad coding work to a full-access subagent that may read or write files and execute commands. <br>
Mitigation: Use a dedicated project directory or sandbox and keep version-control checkpoints before running the skill. <br>
Risk: Parallel agent runs in the same workspace can conflict or overwrite work. <br>
Mitigation: Run parallel builds in separate directories or coordinate file ownership before launching multiple subagents. <br>
Risk: Provider credentials or private sessions may be exposed to delegated coding workflows. <br>
Mitigation: Avoid exposing sensitive credentials unless required and use the least-scoped local OpenCode setup that supports the task. <br>


## Reference(s): <br>
- [OpenCode Game Builder on ClawHub](https://clawhub.ai/jadegaul/opencode-games) <br>
- [jadegaul ClawHub Publisher Profile](https://clawhub.ai/user/jadegaul) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn OpenCode subagents that create or modify project files and run commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
