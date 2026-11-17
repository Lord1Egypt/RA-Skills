## Description:

OpenClaw-native v2 protocol for spec-first multi-agent delivery with explicit phase control, dual review gates, bounded retry and circuit breaker behavior, Lobster approval and recovery, task-store state, and ACP integration for external coding harnesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hakityc](https://clawhub.ai/user/hakityc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate multi-agent delivery workflows that need a stored task spec, explicit phase transitions, separate spec and quality review gates, bounded retries, approval handling, and recoverable execution state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged task-store actions may be unsafe if authorization relies on caller-provided actor or role strings.

Mitigation: Require server-side authenticated identities and capability checks for phase transitions, approval resolution, and circuit opening.

Risk: Reviewers or executors could become de facto workflow authorities if phase ownership is not enforced.

Mitigation: Enforce that only the orchestrator can call phase-transition and circuit-opening actions; reviewers and executors should only record evidence.

Risk: Recovery can become unreliable if execution state is reconstructed from prompt history.

Mitigation: Resume only from persisted task, attempt, approval, checkpoint, and artifact records.

## Reference(s):

- [Multi Agent Protocol ClawHub Page](https://clawhub.ai/hakityc/skills/multi-agent-protocol)
- [task-store Plugin Design](references/task-store-plugin.md)
- [Agent Permission Matrix](references/agent-permissions.md)
- [Migration From v1 To OpenClaw-native v2](references/migration.md)
- [Lobster Approval Recovery Template](lobster/approval-recovery.template.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Protocol guidance for OpenClaw, Lobster, task-store, SQLite event logging, and ACP integration.]

## Skill Version(s):

2.0.0 (source: evidence.json release, artifact/skill.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
