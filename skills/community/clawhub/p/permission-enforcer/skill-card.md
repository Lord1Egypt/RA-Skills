## Description:

Centralizes permission checks for file writes, shell commands, and MCP tool operations using configurable allow, deny, and prompt policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Permission Enforcer to centralize policy checks for workspace file writes, shell command execution, and MCP tool actions. It is intended for environments that need configurable allow, deny, and prompt decisions before potentially sensitive actions run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing or incomplete policy can allow actions by default.

Mitigation: Install with explicit deny and prompt rules for sensitive actions, and test expected boundaries before relying on enforcement.

Risk: The command wrapper may execute reconstructed shell commands unsafely.

Mitigation: Use only in controlled environments unless command execution is hardened to preserve argument boundaries and avoid unsafe shell reconstruction.

Risk: Command logs may contain secrets or sensitive operational details.

Mitigation: Restrict log access and redact or avoid logging sensitive command arguments.

## Reference(s):

- [Permission Enforcer ClawHub page](https://clawhub.ai/woai36d/skills/permission-enforcer)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe permission outcomes such as allow, deny, and prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
