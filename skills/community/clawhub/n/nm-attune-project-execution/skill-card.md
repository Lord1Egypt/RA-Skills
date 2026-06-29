## Description: <br>
Executes implementation plans with progress tracking, checkpoint validation, and quality gates after planning is complete and tasks are ready to implement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill after a plan is ready to execute tasks in dependency order, run validation gates, track progress, manage blockers, and produce completion reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad coding-workflow trigger wording may cause the skill to activate when it is not needed. <br>
Mitigation: Invoke the skill explicitly for planned execution work or narrow trigger wording if activation becomes intrusive. <br>
Risk: Execution guidance can lead to code changes, shell commands, and progress-state updates that affect a project. <br>
Mitigation: Review the implementation plan, commands, and validation results before relying on the changes. <br>


## Reference(s): <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [Nm Attune Project Execution on ClawHub](https://clawhub.ai/athola/skills/nm-attune-project-execution) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, status reports, code blocks, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files and progress state when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
