## Description:

Hive Builder designs, scaffolds, and carefully activates a Hive-style one-person company in OpenClaw using an orchestrator pattern for CEO, governance, and specialist roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moonpoem](https://clawhub.ai/user/moonpoem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to plan or scaffold a contained Hive subsystem, define CEO, HRM, OPS, and specialist role boundaries, and decide when to validate or activate multi-agent routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Hive scaffold or activation plan could change how a workspace is organized or how tasks are routed if adopted too broadly.

Mitigation: Start with planning or a contained scaffold under the workspace's hive directory, and require explicit confirmation before live activation or routing changes.

Risk: Specialist execution could add unnecessary complexity if role separation has not been validated.

Mitigation: Use main-session handling or contained manual validation first, then use sessions_spawn only after the role split is reusable and approved.

Risk: Generated role templates or setup notes may not match an existing workspace's established files and practices.

Mitigation: Review generated role definitions, setup notes, task-state contracts, and security scan results before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moonpoem/skills/hive-builder)
- [Package README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with scaffold plans, role templates, activation checklists, and optional file or shell-command instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to separate planning, scaffolding, validation, and activation, with live routing or specialist spawning gated by explicit user approval.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
