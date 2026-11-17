## Description:

Go (Golang) naming conventions for packages, constructors, structs, interfaces, constants, enums, errors, booleans, receivers, getters/setters, functional options, acronyms, test functions, and subtest names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when writing, reviewing, or refactoring Go code where naming decisions affect readability, exported APIs, or idiomatic Go style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Go and Git command execution, file editing, and delegated agent authority beyond what naming guidance strictly requires.

Mitigation: Install it only in repositories where those actions are acceptable, or restrict usage to read-only review and explicit user-approved validation commands.

Risk: Naming recommendations can trigger API-wide renames or behavior-affecting code edits if applied automatically.

Mitigation: Review proposed renames before applying them, run Go tests and linters afterward, and prefer language-aware rename tooling for project-wide changes.

## Reference(s):

- [Functions, Methods & Options](artifact/references/functions-methods.md)
- [Variables, Booleans, Receivers & Acronyms](artifact/references/identifiers.md)
- [Packages, Files & Import Aliasing](artifact/references/packages-files.md)
- [Test Naming](artifact/references/testing.md)
- [Types, Constants & Errors](artifact/references/types-errors.md)
- [Project Homepage](https://github.com/samber/cc-skills-golang)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with Go code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to Go files and validation commands when the agent harness grants those tools.]

## Skill Version(s):

1.2.0 (source: artifact/SKILL.md metadata.version and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
