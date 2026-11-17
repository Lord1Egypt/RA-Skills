## Description:

Unified TDD skill with three input modes: from spec, from task, or from description, enforcing test-first development using repository patterns, with proptest guidance and backpressure integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imbeasting](https://clawhub.ai/user/imbeasting)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide agents through a strict test-first workflow for implementation work, starting from a spec, task file, or ad-hoc description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create or modify tests and implementation files.

Mitigation: Review generated code changes and test changes before merging or deployment.

Risk: The skill may lead an agent to run local Rust test or coverage commands.

Mitigation: Run commands in the intended local development environment and review command intent before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imbeasting/skills/imbeasting-test-driven-development)
- [Publisher profile](https://clawhub.ai/user/imbeasting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify tests and implementation files, and may propose local Rust test or coverage commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
