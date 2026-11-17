## Description:

Save task checkpoints and file hashes, then resume with a clear next-step list and stale-file warnings. Use for Task Checkpoint and Handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to preserve task goals, completed work, constraints, and selected-file hashes, then resume work or export a handoff with next steps and stale-file warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task notes and exported handoff reports may contain secrets or other sensitive information.

Mitigation: Avoid including secrets in task notes and review handoff files before sharing them.

Risk: Workspace path checks do not provide OS-level isolation.

Mitigation: Retain the host container or sandbox while using the skill.

## Reference(s):

- [Action contract](references/input.md)
- [Task Checkpoint and Handoff on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-task-handoff)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Markdown, JSON, HTML, Checkpoint data]

**Output Format:** [Markdown, JSON, and HTML reports with locally stored checkpoint data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include selected-file hashes and stale-input warnings.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
