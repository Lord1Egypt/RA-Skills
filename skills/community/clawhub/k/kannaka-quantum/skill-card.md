## Description:

Run Kannaka memory operations on quantum backends and help agents use qBraid Lab to inspect environments, manage compute, and launch remote coding agents over SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run OpenQASM circuits, quantum random number generation, and Kannaka resonance recall on qBraid or OpenQuantum backends, with optional qBraid Lab environment, compute, and remote-agent operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask agents to install an unpinned package.

Mitigation: Install only in an isolated environment and pin or review the package version before use.

Risk: Paid quantum hardware and qBraid Lab compute can spend credits, including per-minute compute that continues until stopped.

Mitigation: Require explicit spend approval, set credit ceilings, monitor balances, and stop compute instances immediately after use.

Risk: The skill can use qBraid, OpenQuantum, and agent API credentials.

Mitigation: Use scoped, revocable credentials and remove or rotate secrets after the task completes.

Risk: Remote coding agents can be launched over SSH on provisioned instances.

Mitigation: Launch remote agents only on intended instances, monitor their sessions, and terminate agents plus SSH access when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/kannaka-quantum)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI subcommands return one JSON object on stdout, including errors.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
