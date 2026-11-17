## Description:

Assist with programming tasks using Claude CLI, including project setup, code generation, debugging, refactoring, and code review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leowing](https://clawhub.ai/user/leowing)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide OpenClaw through creating, modifying, debugging, reviewing, and documenting software projects with Claude CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The project setup script can write outside the intended directory or overwrite files if given unsafe paths.

Mitigation: Use only trusted, explicit target directories and safe project names; avoid running the bundled shell script on untrusted input or in directories where overwriting README.md or .gitignore would matter.

## Reference(s):

- [Programming Best Practices Reference](artifact/references/best-practices.md)
- [Code Review Checklist](artifact/references/code-review-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or recommend file edits, project scaffolding, tests, and command execution steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
