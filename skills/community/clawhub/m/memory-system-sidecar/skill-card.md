## Description:

Operates, verifies, rebuilds, and debugs the implemented MemoryLab long-term memory sidecar that feeds active task and live context files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjingh](https://clawhub.ai/user/sjingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a repository's implemented MemoryLab sidecar, including refreshing live context from session history, rebuilding memory indexes, running verification checks, and inspecting memory artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refresh and rebuild workflows can regenerate local memory, context, index, and phase-log artifacts.

Mitigation: Run the skill only in the intended MemoryLab-style repository and review the planned refresh or rebuild command before execution.

Risk: Running the sidecar from a vague request may update working context files when the user only wanted inspection.

Mitigation: Confirm whether the task is inspection, verification, refresh, or rebuild before invoking commands that modify local artifacts.

## Reference(s):

- [Commands](artifact/references/commands.md)
- [Docs Map](artifact/references/docs-map.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may direct agents to run local refresh, rebuild, verification, and inspection commands for the MemoryLab memory sidecar.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
