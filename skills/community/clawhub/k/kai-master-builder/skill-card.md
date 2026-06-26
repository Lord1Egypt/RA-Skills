## Description: <br>
Kai Master Builder guides agents through planning, task tracking, and execution for app, feature, and fix development, with optional cron or user-driven automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a software goal into a structured project plan, task list, build prompt, and iterative implementation workflow that can continue across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad project-execution workflows may modify files or run validation commands beyond the user's immediate intent. <br>
Mitigation: Keep normal agent approval prompts enabled and review generated plans, commands, and file changes before accepting them. <br>
Risk: Cron or unattended operation can persist automation in a workspace over time. <br>
Mitigation: Enable autonomous operation only in workspaces that are appropriate for automation, and regularly review the generated task and changelog files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ogdegenblaze/kai-master-builder) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown project plans, task lists, build prompts, and inline command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files such as PROJECT_PLAN.md, PROJECT_TASKS.md, PROJECT_CHANGELOG.md, and PROJECT_README.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
