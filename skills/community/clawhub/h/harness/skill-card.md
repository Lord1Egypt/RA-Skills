## Description:

This skill should be used for multi-session autonomous agent work requiring progress checkpointing, failure recovery, and task dependency management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use harness to coordinate long-running, multi-session agent work with checkpointed progress, dependency-aware task selection, recovery after interrupted sessions, and optional concurrent workers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad automatic control over a repository, including rollback and cleanup behavior that may remove uncommitted work.

Mitigation: Install only in dedicated projects or isolated worktrees where repository-wide rollback is acceptable, and keep important work committed or backed up.

Risk: Task-supplied validation and cleanup commands may execute unintended or unsafe commands.

Mitigation: Review harness-tasks.json before runs and do not let untrusted users edit validation or cleanup commands.

Risk: Stop and idle hooks can block an agent from stopping or continue post-run self-reflection when that behavior is not desired.

Mitigation: Disable or remove the hooks, or remove the activation marker, when continuous task enforcement is not appropriate.

## Reference(s):

- [ClawHub skill release: harness](https://clawhub.ai/eohmig/skills/harness)
- [ClawHub publisher profile: eohmig](https://clawhub.ai/user/eohmig)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON state examples, and hook command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains progress and task-state files when activated; hooks may emit JSON block decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
