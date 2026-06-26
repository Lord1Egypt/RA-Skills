## Description: <br>
Spawns an isolated Project Coordinator session that owns a project's context, breaks work into tasks, and spawns subagents for parallel execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaigegao1110](https://clawhub.ai/user/kaigegao1110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to coordinate complex projects by defining scope, splitting work into parallel subagent tasks, monitoring progress, and compiling final deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The coordinator and its subagents can read workspace files, run shell commands, and create or modify project artifacts. <br>
Mitigation: Install only in workspaces where that level of agent access is acceptable, keep project goals narrow, and review changes before relying on them. <br>
Risk: Archiving depends on the archive-project skill and may touch sensitive project history. <br>
Mitigation: Review the archive-project dependency and require checkpoints before archiving or handling sensitive work. <br>


## Reference(s): <br>
- [Project Coordinator homepage](https://github.com/KaigeGao1110/Project-Coordinator) <br>
- [ClawHub release page](https://clawhub.ai/kaigegao1110/project-coordinator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, task plans, inline shell commands, and project artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify workspace files and delegate tasks to subagents when the agent runtime grants those tools.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
