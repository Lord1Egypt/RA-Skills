## Description:

Verify the bead daemon is alive and responsive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and operators who use the beads system can use this skill to check whether the local bead daemon is running and accepting connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local beads environment and the bd command being present.

Mitigation: Install only where the beads system is expected and verify bd is available in PATH before use.

Risk: The health check is limited to daemon responsiveness and does not diagnose broader system state.

Mitigation: Treat the result as a narrow daemon availability check and perform additional diagnostics for operational incidents.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local bd command and bead daemon socket.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
