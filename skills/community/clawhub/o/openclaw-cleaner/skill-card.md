## Description:

OpenClaw Cleaner provides project directory maintenance helpers for snapshots, diffs, checkpoints, task progress tracking, health checks, skill matching, backups, and markdown optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[computersniper](https://clawhub.ai/user/computersniper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and maintain OpenClaw workspaces, create local snapshots and backups, compare changes, track batch task progress, and optimize selected markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly copy and rewrite sensitive workspace and agent-state files.

Mitigation: Use it only in workspaces where copying full file contents into .cleaner-backups is acceptable, and avoid running it around secrets or private agent memory.

Risk: Restore and optimization actions can overwrite local files or reduce markdown content without clear confirmation.

Mitigation: Require manual review before backup.restore, optimize.soul, or optimize.full, and inspect diffs or backups before accepting changes.

Risk: The local read/write authority is broad and path containment is under-controlled.

Mitigation: Run the skill in a bounded workspace with least-privilege file access and review the artifact before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/computersniper/skills/openclaw-cleaner)
- [Publisher profile](https://clawhub.ai/user/computersniper)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Files]

**Output Format:** [JSON objects and markdown/text reports from exported helper calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local backup, snapshot, checkpoint, progress, and optimized markdown files in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
