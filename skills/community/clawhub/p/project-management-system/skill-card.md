## Description:

A comprehensive project management system for AI agents. Manage projects from initiation to delivery with structured workflows, templates, quality gates, and role-based operation manuals. Supports both dispatcher and executor roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don068589](https://clawhub.ai/user/don068589)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and teams use this skill to plan, dispatch, track, review, and close projects through structured project briefs, task specifications, quality gates, status records, risk registers, and final reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included system-check restore flow can discard uncommitted changes in the detected Git root.

Mitigation: Do not run tools/system-check.py --restore unless you have a backup or clean stash and have verified the Git root.

Risk: Resource-profile feedback and 'remember for future' notes can persist into future work and influence later agent behavior.

Mitigation: Review these items as untrusted inputs before accepting them as accumulated rules or collaboration profiles.

Risk: The skill may require file-write, shell, timer, Heartbeat, or multi-agent authority during normal project operation.

Mitigation: Install and run it in an isolated workspace, granting each authority deliberately.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/don068589/skills/project-management-system)
- [README](README.md)
- [Dispatcher Operations Manual](docs/coordinator.md)
- [Executor Operations Manual](docs/executor.md)
- [Quality Assurance Mechanism](docs/quality.md)
- [Task Management Mechanism](docs/task-management.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, structured checklists, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable templates for project briefs, task specifications, review records, risk registers, status reports, change requests, milestone reports, and final reports.]

## Skill Version(s):

1.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
