## Description:

Parallel Orchestrate shreds a finished gstack implementation plan into wave-based subtasks, dispatches parallel Claude Code subagents in isolated git worktrees, verifies each wave, and hands off to review and shipping skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to execute an approved implementation plan by decomposing work into parallel tasks, coordinating isolated subagents, validating each wave, and preparing the branch for review and shipping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has high-impact repository mutation authority because it can spawn parallel coding agents, run repository test and lint commands, and cherry-pick subagent commits.

Mitigation: Use it in trusted repositories, review the generated TASKS.md before approving dispatch, and inspect diffs before shipping.

Risk: Custom test or lint commands and unusual branch names can increase execution and state-handling risk.

Mitigation: Approve only expected commands, avoid unusual branch names for orchestration runs, and review command output at each wave gate.

Risk: Telemetry is local-first but may send remote telemetry through the existing gstack telemetry binary when the user has opted in.

Mitigation: Keep telemetry disabled unless the repository owner accepts that behavior, and review gstack telemetry settings before use.

## Reference(s):

- [Parallel Orchestrate GitHub Repository](https://github.com/kaicianflone/parallel-orchestrate)
- [Parallel Orchestrate ClawHub Skill Page](https://clawhub.ai/kaicianflone/skills/parallel-orchestrate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command blocks and JSONL orchestration state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task breakdowns, wave verification guidance, subagent dispatch prompts, state files, and final handoff reports.]

## Skill Version(s):

1.6.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
