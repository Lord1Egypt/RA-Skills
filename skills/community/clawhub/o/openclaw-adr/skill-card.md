## Description:

Architecture Decision Records (ADR) management. Creates, updates, and tracks architectural decisions with templates and linting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, update, list, and lint Architecture Decision Records in MADR-style markdown so architectural choices can be tracked in a project repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates ADR markdown files in docs/adr under the selected project root.

Mitigation: Run it from the intended repository root, review generated ADR files before committing, and keep normal version-control backups.

Risk: Permission scope is not declared separately from the skill behavior.

Mitigation: Before installation, confirm that local project-file creation and modification under docs/adr is acceptable for the target workspace.

## Reference(s):

- [MADR](https://adr.github.io/madr/)
- [OpenClaw ADR on ClawHub](https://clawhub.ai/michealxie001/skills/openclaw-adr)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown ADR files, command-line text, JSON configuration examples, and YAML CI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and modifies ADR markdown files under docs/adr in the selected project root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
