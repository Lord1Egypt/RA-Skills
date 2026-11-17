## Description:

Teaches an agent how to list, inspect, diff, and restore Plakar snapshots for filesystem recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misterflop](https://clawhub.ai/user/misterflop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide an agent through Plakar snapshot listing, inspection, comparison, and restore operations after a filesystem change needs to be reviewed or rolled back.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore workflows can overwrite live files, especially when triggered by broad rollback requests.

Mitigation: Require the agent to identify the exact snapshot, path, and destination, ask for explicit confirmation, and prefer restoring to a separate directory unless live overwrite is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misterflop/skills/plakar-backup)
- [ClawHub publisher profile](https://clawhub.ai/user/misterflop)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Restore guidance should identify the exact snapshot, path, and destination before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
