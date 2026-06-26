## Description: <br>
Long Task Manager helps OpenClaw agents manage long-running work with local task submission, file-backed status tracking, progress updates, cancellation markers, and result retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevinYxl](https://clawhub.ai/user/DevinYxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to coordinate long-running OpenClaw agent tasks, monitor progress, cancel work, and retrieve persisted results across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task configs, progress details, and result summaries are persisted as local JSON files and can contain sensitive data if callers include it. <br>
Mitigation: Use a private task directory and avoid storing secrets or sensitive personal data in task configs, progress details, or result summaries. <br>
Risk: Task and agent identifiers are used in local task records and paths. <br>
Mitigation: Use trusted task and agent identifiers and keep task directory permissions restricted to the intended local user or service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DevinYxl/long-task-manager) <br>
- [Skill documentation](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown documentation with Python code snippets, shell commands, YAML configuration, and local JSON task records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configurable local task directory for task configs, status, cancellation markers, and result files; no network output is described in the evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact documentation and package metadata show 1.0.0/v1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
