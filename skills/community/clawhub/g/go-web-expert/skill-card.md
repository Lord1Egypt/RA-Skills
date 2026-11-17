## Description:

Comprehensive Go web development persona enforcing zero global state, explicit error handling, input validation, testability, and documentation conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building or changing Go web applications, especially HTTP handlers and services that need explicit dependency injection, validation, error handling, tests, and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is opinionated about Go web API structure and may propose patterns that do not fit an existing architecture.

Mitigation: Review generated code for fit with the application's established architecture before adopting it.

Risk: Generated handler or validation changes can introduce incorrect behavior if accepted without project-specific review.

Mitigation: Run the relevant Go tests and review validation, error handling, and response behavior before deployment.

## Reference(s):

- [Go Web Expert on ClawHub](https://clawhub.ai/anderskev/skills/go-web-expert)
- [Testing Go HTTP Handlers](artifact/references/testing-handlers.md)
- [Input Validation with go-playground/validator](artifact/references/validation.md)

## Skill Output:

**Output Type(s):** [guidance, code, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opinionated guidance for Go web API structure, validation, handler tests, and documentation conventions.]

## Skill Version(s):

2.3.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
