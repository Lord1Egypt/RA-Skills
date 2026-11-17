## Description:

Manages long-running, multi-session goals by maintaining a single persistent goal.md with sub-goals, checkpoints, decisions, and evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzusp](https://clawhub.ai/user/zzusp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, researchers, operators, and writers use this skill to keep long-running work recoverable across turns, sessions, and context compaction. It guides the agent to maintain one authoritative goal.md with current sub-goals, checkpoints, decisions, progress, evidence, and remaining open items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update a persistent goal.md in the workspace, which may be undesirable in repositories with strict file governance.

Mitigation: Review and confirm the authoritative goal.md path before first use, and keep the file within the workspace's accepted artifact location.

Risk: The validator and template require specific Chinese section names and fields, so incompatible goal.md formatting can fail validation.

Mitigation: Start from artifact/assets/goal-template.md and run artifact/scripts/validate_long_goal.py --goal <goal.md path> before handoff or delivery.

## Reference(s):

- [Goal template](artifact/assets/goal-template.md)
- [Long-goal validator](artifact/scripts/validate_long_goal.py)
- [ClawHub skill page](https://clawhub.ai/zzusp/skills/long-goal)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with goal.md updates and validator shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a canonical workspace goal.md and points to evidence or validation artifacts when progress is recorded.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
