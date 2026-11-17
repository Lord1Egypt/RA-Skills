## Description:

Run slow local commands and queues with bounded logs, safe recovery, and artifact checks. Use for rendering, TTS, batch processing, builds, and submitted remote jobs; also offer fresh-chat handoffs and reusable skills when a completed runner-assisted task is followed by independent new work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhzyw](https://clawhub.ai/user/dhzyw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use this skill to run long local or already-submitted remote jobs while keeping the agent focused on planning, exception handling, and final review. It is suited for builds, rendering, media processing, data jobs, downloads, and other slow command queues that need bounded logs, status checks, and artifact validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job specifications run local commands and should be treated as equivalent to running those commands manually.

Mitigation: Inspect every job spec and script before execution, use reviewed or pinned releases, and avoid running untrusted specs.

Risk: Launched commands inherit the local execution environment and logs may contain sensitive output from child commands.

Mitigation: Use separate job directories, avoid placing secrets in job specs or command output, and read only bounded log excerpts when needed.

Risk: Automatic replay can repeat side effects if a task is not truly idempotent.

Mitigation: Enable replay only for tasks explicitly declared safe, keep external or paid operations non-replayable, and recheck completed artifacts before skipping them.

Risk: Remote watching observes an existing job but does not cancel remote execution or billing.

Mitigation: Persist a reliable remote job ID, use the watcher only for authorized read-only status checks, and verify remote outputs before treating the task as complete.

## Reference(s):

- [Long Task Runner Skill Instructions](SKILL.md)
- [Job Configuration and Interfaces](references/job-spec.md)
- [Scenario Guidance](references/scenarios.md)
- [Host Waiting Boundaries](references/host-waiting.md)
- [Task Handoff Guidance](references/task-handoff.md)
- [Optional Compression Guidance](references/optional-compression.md)
- [Task Handoff Template](assets/task-handoff-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON job specifications and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local job specifications, bounded status summaries, log excerpts, and artifact-check guidance for the agent to review.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
