## Description:

Clean up node_modules and .next folders to free up disk space using npkill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashirbadgudu](https://clawhub.ai/user/ashirbadgudu)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to identify and remove accumulated JavaScript dependency folders and Next.js build artifacts from development workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk deletion can remove dependency or build artifact folders that are still needed.

Mitigation: Run dry-run first, prefer interactive selection, and use automated deletion only after reviewing matched paths.

Risk: Running cleanup from a broad filesystem location can match unintended projects or directories.

Mitigation: Run the skill from a narrow development workspace or pass an explicit search directory.

Risk: The skill depends on installing npkill from the configured npm registry.

Mitigation: Install only when the npm registry source is trusted and acceptable for the environment.

## Reference(s):

- [NPkill on ClawHub](https://clawhub.ai/ashirbadgudu/skills/npkill)
- [Publisher profile](https://clawhub.ai/user/ashirbadgudu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for developer workspaces and should be reviewed before deletion.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
