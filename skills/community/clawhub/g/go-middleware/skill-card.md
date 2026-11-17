## Description:

Idiomatic Go HTTP middleware patterns with context propagation, structured logging via slog, centralized error handling, and panic recovery. Use when writing middleware, adding request tracing, or implementing cross-cutting concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when designing or reviewing Go HTTP middleware for request context propagation, structured request logging, centralized error handling, panic recovery, and middleware-chain correctness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Request metadata or tracing headers may expose identifiers when copied into production systems or forwarded to untrusted downstream services.

Mitigation: Review outbound request destinations and only propagate request IDs, user metadata, and tenant metadata to trusted services.

Risk: Logging and panic-recovery examples can retain tokens, credentials, personal data, internal paths, or raw panic details if adapted without filtering.

Mitigation: Sanitize structured log fields, keep panic details out of client responses, and restrict broad log retention or export.

Risk: Incorrect middleware ordering or a missing next-handler call can bypass recovery, produce misleading status logs, or drop requests.

Mitigation: Use the documented gates to verify recovery wraps the chain, status-aware middleware passes the wrapped ResponseWriter, and every forward path calls next or clearly returns a response.

## Reference(s):

- [Context Propagation in Go Middleware](references/context-propagation.md)
- [Structured Logging with slog](references/structured-logging.md)
- [Centralized Error Handling and Recovery Middleware](references/error-handling-middleware.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with Go code snippets and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; does not require hidden execution or external services.]

## Skill Version(s):

2.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
