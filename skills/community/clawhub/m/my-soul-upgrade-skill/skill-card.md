## Description:

Manage and synchronize global and agent-specific Soul definitions using a two-layer template system with automated rebuild scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to update and synchronize global and per-agent Soul instruction definitions across agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent changes to global or agent-specific Soul instruction files.

Mitigation: Review diffs before syncing, keep backups of SOUL.md and template.md, and avoid the global update path unless every agent should receive the change.

Risk: Manual edits can leave generated Soul files out of sync with their templates.

Mitigation: Run the documented build_all_souls.py sync step after intentional template changes and verify the regenerated agent files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-soul-upgrade-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with ordered procedures and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide updates to persistent OpenClaw instruction files; review resulting diffs before applying changes.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
