## Description:

Organize discussed or evolving development, repair, testing, research, migration, or complex operational work into an executable, resumable, independently reviewable task documentation package, then derive a launch configuration from the current request and relevant task-family history for user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukp20](https://clawhub.ai/user/xukp20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn complex, evolving implementation, repair, testing, migration, operations, or research work into durable task packages with frozen decisions, work items, execution receipts, review records, and launch configuration. It is intended for tasks that need resumable coordination and review, not short one-off requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository context and may create local task-package markdown files when asked to record work.

Mitigation: Review and confirm the parent directory, launch configuration, and cleanup policy before execution; the inspected helper script refuses to overwrite an existing task directory.

Risk: Worker, reviewer, worktree, and external-action choices can affect repository state if a user confirms execution without checking the proposed configuration.

Mitigation: Use the skill's confirmation gate to review worker and reviewer topology, branch or worktree plan, validation scope, and any real provider, server, migration, release, or push action before starting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xukp20/skills/organize-task-package)
- [Server-resolved GitHub provenance](https://github.com/xukp20/codex-task-package/tree/main/skills/organize-task-package)
- [Discussion Recovery and Task Design](references/design-and-planning.md)
- [Task Package Structure and Initialization](references/package-structure.md)
- [Launch Configuration Recommendation and Confirmation](references/launch-configuration.md)
- [Worker and Reviewer Session Topology](references/session-topology.md)
- [Worker Execution and Review](references/execution-and-review.md)
- [Parallel Worker Orchestration](references/parallel-orchestration.md)
- [Task-Type Profiles](references/task-profiles.md)
- [Lessons from Existing Task Records](references/observed-lessons.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown task package documents with optional shell commands and configuration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local task-package scaffolds and review records when explicitly authorized; does not authorize implementation, external actions, or overwrites by itself.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
