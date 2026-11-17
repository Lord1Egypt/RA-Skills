## Description:

Assists test-driven development by generating test scaffolds, running Python tests, reporting coverage, and guiding red-green-refactor workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate test scaffolds, run Python test suites, inspect coverage, and structure test-driven development work in supported repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Test, status, and coverage commands can execute code from the target project.

Mitigation: Use the skill only in trusted repositories or isolated environments and review commands before running them.

Risk: The release advertises Jest, Go, mutation testing, and full TDD-cycle support that the shipped artifact does not provide.

Mitigation: Validate required framework support before adoption and do not depend on those advertised features unless they are independently present.

Risk: A writable sibling c-support directory could affect optional C/Unity behavior.

Mitigation: Install the skill in a trusted, non-shared location and review sibling support libraries before using C/Unity generation.

Risk: Report files are written under /tmp and are not suitable for high-integrity automation.

Mitigation: Treat /tmp reports as convenience output only and use isolated workspaces or dedicated report paths for controlled automation.

## Reference(s):

- [OpenClaw TDD Assistant on ClawHub](https://clawhub.ai/michealxie001/skills/oc-tdd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with generated test code, shell commands, coverage summaries, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated test files when an output path is provided; test and coverage commands execute in the target repository.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
