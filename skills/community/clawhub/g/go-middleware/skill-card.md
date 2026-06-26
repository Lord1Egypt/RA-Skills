## Description: <br>
Idiomatic Go HTTP middleware patterns with context propagation, structured logging via slog, centralized error handling, and panic recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, review, and implement Go HTTP middleware for request context propagation, structured logging, centralized error handling, panic recovery, and middleware chain ordering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the logging and recovery examples without review could expose secrets, tokens, sensitive request data, or unrestricted panic stack traces in broadly accessible logs. <br>
Mitigation: Review production logging policy before deployment and redact or avoid sensitive request data, credentials, and unrestricted stack traces. <br>


## Reference(s): <br>
- [Context Propagation in Go Middleware](references/context-propagation.md) <br>
- [Centralized Error Handling and Recovery Middleware](references/error-handling-middleware.md) <br>
- [Structured Logging with slog](references/structured-logging.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Go code examples and review checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for Go HTTP middleware patterns.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
