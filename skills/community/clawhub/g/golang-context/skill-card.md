## Description:

Idiomatic context.Context usage in Golang \u2014 propagation through API boundaries, cancellation, timeouts and deadlines, request-scoped values, context.WithoutCancel for background work outliving requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when designing, reviewing, or debugging Go context propagation across HTTP handlers, service layers, databases, external API calls, goroutines, cancellation paths, and request-scoped values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad git and agent permissions beyond what its Go context guidance normally requires.

Mitigation: Install only after reviewing requested permissions, and prefer a release with git access narrowed to read-only commands or removed and Agent access removed unless delegation is required.

Risk: Generated guidance or file edits could introduce incorrect context propagation, cancellation, timeout, or request-value patterns into Go code.

Mitigation: Review proposed changes before applying them and run Go tests, static analysis, and relevant linters such as govet or staticcheck.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-context)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Cancellation, Timeouts & Deadlines](references/cancellation.md)
- [Context in HTTP Servers & Service Calls](references/http-services.md)
- [Context Values & Cross-Service Tracing](references/values-tracing.md)
- [Project homepage](https://github.com/samber/cc-skills-golang)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Go code examples and occasional shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Go source files and may propose edits to project files.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
