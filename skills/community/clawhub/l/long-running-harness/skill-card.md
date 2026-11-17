## Description:

A Chinese-language workflow harness that helps agents create, manage, delegate, resume, and report progress on long-running project tasks across multiple context windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up persistent project state, track feature completion, standardize session start and end routines, delegate scoped subagent work, schedule progress checks, and generate project status reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow normalizes running initialization scripts, installing dependencies, initializing databases, and starting background services.

Mitigation: Inspect dependency manifests, init.sh, init_db.sh, npm scripts, and service commands before execution; require explicit approval for installs, database changes, and background services.

Risk: Delegated subagent work and recurring scheduled agent turns can continue project activity without enough user control.

Mitigation: Review delegated task payloads and cron schedules before use; keep scopes narrow, use timeouts, and require explicit approval for recurring scheduled agent turns.

Risk: The skill relies on project state files that may become stale, incomplete, or incorrectly marked as passing.

Mitigation: Read progress.md, features.json, and recent git history at session start, then run the documented validation steps before marking any feature as complete.

## Reference(s):

- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [feature-list-template.md](references/feature-list-template.md)
- [init-template.md](references/init-template.md)
- [progress-log-template.md](references/progress-log-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON structures and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project workflow files, status summaries, task delegation prompts, and operational routines when applied by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
