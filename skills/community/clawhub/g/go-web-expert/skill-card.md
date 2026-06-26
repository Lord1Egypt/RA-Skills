## Description: <br>
Comprehensive Go web development persona enforcing zero global state, explicit error handling, input validation, testability, and documentation conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building or reviewing Go web applications that need explicit dependency injection, validation at HTTP boundaries, wrapped error handling, handler tests, and Go documentation conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited Go code may affect database-backed tests, fixtures, or golden files. <br>
Mitigation: Review generated code normally before running database-backed tests or accepting fixture and golden-file updates. <br>
Risk: The skill enforces strong conventions that may be stricter than an existing Go web project's style. <br>
Mitigation: Apply the guidance against the project's own requirements and review proposed changes before merging. <br>


## Reference(s): <br>
- [Validation Reference](references/validation.md) <br>
- [Testing Go HTTP Handlers](references/testing-handlers.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/go-web-expert) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with Go code examples and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no code execution or external tool access is requested by the skill.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
