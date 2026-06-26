## Description: <br>
Autonomous overnight work agent that accepts a task before sleep and returns structured results by morning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and productivity-focused users use this skill to delegate research, writing, data organization, and code review tasks for unattended execution with a morning summary and deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended execution may read task-relevant files, perform web research, and write reports without real-time user review. <br>
Mitigation: Run the skill only on tasks and workspaces appropriate for unattended processing, and review generated summaries and deliverables before relying on them. <br>
Risk: Telegram or webhook notifications may expose task names, summaries, and output paths to third-party services. <br>
Mitigation: Use local macOS notifications for sensitive work, and avoid external notification channels when task metadata or output locations are confidential. <br>
Risk: The artifact describes a /tmp fallback on file-write failure even though normal operation is intended to stay under the work directory. <br>
Mitigation: Confirm output locations after each run and restrict deployment policy to the documented ~/overnight-output work directory when sensitive files are involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fullstackcrew-alpha/overnight-worker) <br>
- [Output format specifications](references/output-formats.md) <br>
- [Task templates](references/task-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, CSV, JSON, shell commands, progress logs, and notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped work directories under ~/overnight-output with PLAN.md, progress.log, morning-summary.md, and task-specific deliverables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
