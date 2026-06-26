## Description: <br>
Helps agents manage complex, multi-step work by creating and maintaining persistent markdown planning files across a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingcd](https://clawhub.ai/user/yingcd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill for long-running implementation, research, or multi-phase tasks where goals, findings, decisions, progress, and errors need to survive context resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists task context in local markdown files, which may capture sensitive project details if users include them. <br>
Mitigation: Avoid placing secrets in task_plan.md, findings.md, or progress.md, and delete those files when the saved context is no longer needed. <br>
Risk: The skill includes shell scripts that create and inspect planning files in the active workspace. <br>
Mitigation: Review scripts/init-session.sh and scripts/check-complete.sh before enabling runtime execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yingcd/planning-with-files-from-github) <br>
- [Workflow Reference](artifact/references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown planning files with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates task_plan.md, findings.md, and progress.md in the active workspace when initialized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
