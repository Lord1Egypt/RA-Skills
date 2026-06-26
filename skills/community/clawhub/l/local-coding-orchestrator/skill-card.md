## Description: <br>
Use OpenClaw as a supervisor-driven orchestration scaffold for local coding CLIs such as Codex, Claude Code, and OpenCode. Supports task records, lifecycle transitions, worker launch and reconcile, retry briefs, pipeline presets, and environment-aware blocking for local coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijiejoy](https://clawhub.ai/user/lijiejoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate local coding work across Codex, Claude Code, and OpenCode through task records, worker roles, lifecycle states, review phases, and retry briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The usage guide shows PowerShell execution with an execution-policy bypass, which can run local scripts that users have not independently reviewed. <br>
Mitigation: Review the referenced PowerShell scripts before installing or running them, use the bypass form only for code you trust, and prefer a normal PowerShell execution path when it works. <br>
Risk: Worker processes may exit or report success before objective checks prove the task is complete. <br>
Mitigation: Use the documented done policies, review artifacts, and supervisor lifecycle transitions before marking work completed. <br>
Risk: Local CLI workers may run in constrained, read-only, or path-drifted environments where outputs do not land in the intended repo. <br>
Mitigation: Verify the reachable workdir, preserve logs and task records, classify environment blockers explicitly, and relaunch with corrected paths when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lijiejoy/local-coding-orchestrator) <br>
- [Usage Guide](docs/usage-guide.md) <br>
- [Operator Playbook](docs/operator-playbook.md) <br>
- [Task Schema v1](docs/task-schema.v1.json) <br>
- [Supervisor vs Worker Responsibilities](assets/references/supervisor-vs-worker.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON task records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces supervisor-facing task structure, worker briefs, lifecycle decisions, retry guidance, and operational summaries; it does not directly guarantee that delegated code changes land.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata; artifact changelog top entry is v0.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
