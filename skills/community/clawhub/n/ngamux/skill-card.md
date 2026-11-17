## Description:

Build and modify web services using ngamux, a simple HTTP router for Go. Define routes, apply middleware, handle requests, and send responses efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hadihammurabi](https://clawhub.ai/user/hadihammurabi)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build, modify, and debug Go web services that use the ngamux router for HTTP routes, middleware, request parsing, responses, and route grouping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated route handlers or middleware may omit ordinary web security controls such as authentication, input validation, upload limits, or response escaping.

Mitigation: Review generated Go code and configuration for the security controls called out in the ClawHub security guidance before deployment.

Risk: The artifact is documentation-only and the scanner found no suspicious behavior, but its guidance can still lead to incorrect application code if applied without review.

Mitigation: Treat outputs as implementation guidance and test handlers, middleware chains, request parsing, and responses in the target application.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Go examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for Go HTTP routing, middleware, request handling, response construction, configuration, and debugging.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
