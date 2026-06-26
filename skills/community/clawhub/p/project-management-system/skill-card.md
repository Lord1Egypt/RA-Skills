## Description: <br>
A comprehensive project management system for AI agents that manages projects from initiation to delivery with structured workflows, templates, quality gates, and role-based operation manuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[don068589](https://clawhub.ai/user/don068589) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents, project leads, and task executors use this skill to plan projects, break work into tasks, dispatch execution, review deliverables, track risk, and carry projects from initiation to acceptance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad autonomous project-maintenance behavior, including managing project state files, dispatching work, reviewing deliverables, and using heartbeat or timer-style continuation. <br>
Mitigation: Scope the skill to dedicated project directories, review task specifications before execution, and keep human approval checkpoints for initiation, major changes, subjective outputs, and final acceptance. <br>
Risk: The optional restore helper can erase uncommitted and untracked repository work. <br>
Mitigation: Do not allow `tools/system-check.py --restore` unless a human has inspected `git status` and accepts the loss of uncommitted and untracked work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/don068589/project-management-system) <br>
- [README](README.md) <br>
- [Dispatcher operations manual](docs/coordinator.md) <br>
- [Executor operations manual](docs/executor.md) <br>
- [Quality gates](docs/quality.md) <br>
- [Runtime self-sustaining mechanism](docs/runtime.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown guidance, reusable Markdown templates, and optional Python tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured project briefs, task specifications, review records, status reports, risk registers, final reports, and optional dashboard or integrity-check output.] <br>

## Skill Version(s): <br>
1.6.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
