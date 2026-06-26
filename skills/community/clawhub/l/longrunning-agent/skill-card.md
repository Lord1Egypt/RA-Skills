## Description: <br>
Enables AI agents to maintain continuity for long-running projects by tracking progress, task dependencies, and incremental work across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YonghaoZhao722](https://clawhub.ai/user/YonghaoZhao722) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to manage long-running project work across sessions, including selecting tasks, recording progress, testing changes, and committing incremental work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local setup scripts and agent-made commits can change the project environment or repository history. <br>
Mitigation: Review any init.sh before execution and inspect file changes before accepting commits. <br>
Risk: Progress logs, task files, session output, or web UI synchronization may capture sensitive project details. <br>
Mitigation: Avoid placing secrets in workflow logs and confirm storage or synchronization behavior before using the skill on private work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YonghaoZhao722/longrunning-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update project workflow files such as CLAUDE.md, task.json, progress.txt, and optional init.sh.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
