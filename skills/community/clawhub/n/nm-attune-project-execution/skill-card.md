## Description: <br>
Executes implementation plans with progress tracking, checkpoint validation, and quality gates for agents working from ready-to-implement task plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill after planning is complete to execute implementation tasks, track progress, validate checkpoints, manage blockers, and produce completion reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as execution, implementation, and tdd may activate this workflow during general repository work. <br>
Mitigation: Confirm the user has a ready implementation plan before applying the full workflow. <br>
Risk: The skill may lead an agent to propose code changes or command runs that affect a repository. <br>
Mitigation: Review proposed code changes and command runs before execution, especially quality gate and test commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-project-execution) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, checklist, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task status updates, quality gate checklists, validation commands, blocker reports, execution-state JSON, and mission reports.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
