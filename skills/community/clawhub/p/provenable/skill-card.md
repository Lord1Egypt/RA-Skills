## Description:

A condensed single-file guide for operating and integrating AEGX Provenable, a runtime that helps agents make risky behavior observable, verifiable, and recoverable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, integrators, and operators use this skill to understand, integrate, and operate AEGX Provenable workflows for guarded agent actions, runtime health checks, snapshots, evidence export, and incident review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a condensed guide and is not proof that the full AEGX Provenable runtime code is safe.

Mitigation: Obtain the actual repository from a trusted source and review the installer, daemon, adapters, and runtime code before building or running it.

Risk: The referenced daemon and adapters may store records, run background processes, and monitor local activity.

Mitigation: Confirm record storage locations, process behavior, and monitoring scope before installation or operational use.

Risk: Using the runtime while protection is degraded can create false confidence in guarded actions.

Mitigation: Check daemon status and run active self-verification before high-risk work; pause risky actions if protection is stale, unreachable, or uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoojunwei/skills/provenable)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with command examples and structured operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Condensed single-file repository guide; it does not include raw source code.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
