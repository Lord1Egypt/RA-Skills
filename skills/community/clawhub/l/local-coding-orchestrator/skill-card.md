## Description:

Use OpenClaw as a supervisor-driven orchestration scaffold for local coding CLIs such as Codex, Claude Code, and OpenCode, with support for task records, lifecycle transitions, worker launch and reconcile, retry briefs, pipeline presets, and environment-aware blocking for local coding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijiejoy](https://clawhub.ai/user/lijiejoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering operators use this skill to supervise local coding work across Codex, Claude Code, and OpenCode with task records, worker roles, review loops, retries, and objective completion checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PowerShell examples use ExecutionPolicy Bypass and relative script paths.

Mitigation: Verify scripts from a trusted installed path before execution, avoid ExecutionPolicy Bypass where possible, and prefer explicit absolute paths.

Risk: The package references local worker scripts that security evidence says are missing from the package.

Mitigation: Confirm the required worker adapters exist in the installed skill before enabling launch or auto-launch behavior.

Risk: Auto-launching local coding workers can modify repositories and create sensitive local prompts, logs, results, and summaries.

Mitigation: Use preview or manual modes first, isolate the target repo or worktree, and treat generated orchestration artifacts as sensitive.

Risk: The artifact documentation describes the skill as an experimental scaffold with heuristic background reconciliation and incomplete build/test parsing.

Mitigation: Use objective checks, review phases, and manual validation before marking work completed or relying on unattended execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijiejoy/skills/local-coding-orchestrator)
- [Publisher profile](https://clawhub.ai/user/lijiejoy)
- [Usage guide](docs/usage-guide.md)
- [Operator playbook](docs/operator-playbook.md)
- [Capability map](docs/capability-map.md)
- [Task schema](docs/task-schema.v1.json)
- [Status](docs/status.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell command examples, JSON task records, worker briefs, logs, summaries, and review artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local orchestration and may include paths to prompt, log, result, summary, and review artifacts.]

## Skill Version(s):

0.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
