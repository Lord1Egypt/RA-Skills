## Description:

Guides agents through implementing or refactoring code to conform to an approved docs/architecture contract, with pre-flight checks, pattern coverage planning, NFR verification, and human approval gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inetgas](https://clawhub.ai/user/inetgas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when application code must be built or refactored against an approved architecture package. It helps agents enforce selected patterns, functional coverage, non-functional requirements, smoke tests, and review gates before declaring implementation complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project architecture and requirement files and help modify application code.

Mitigation: Use it only in repositories where the arch-compiler workflow is intended, and review implementation plans and code changes before accepting them.

Risk: The workflow references a local ~/.codex/arch-compiler helper.

Mitigation: Verify the local arch-compiler installation is trusted before allowing the helper to run.

## Reference(s):

- [arch-compiler homepage](https://github.com/inetgas/arch-compiler)
- [ClawHub skill page](https://clawhub.ai/inetgas/skills/implementing-architecture)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with task plans, checklists, commands, and code or configuration changes when implementation proceeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires terminal access and human confirmation at architecture and implementation gates.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
