## Description:

Provides an unofficial typed Go client and usage guidance for calling Render’s public REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the Go package to call Render’s API from Go projects, including listing resources and managing services, deployments, and related infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some API operations can change live infrastructure, including deploying, suspending, scaling, updating, or deleting services.

Mitigation: Call those operations only for services the user named and only when the user asked for that action.

Risk: The Render API key grants access to account resources.

Mitigation: Read the key from an environment variable; do not hardcode, commit, log, or print request headers containing it.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Project repository](https://github.com/psyb0t/go-render-api)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-render-api)
- [Render pagination documentation](https://api-docs.render.com/reference/pagination)

## Skill Output:

**Output Type(s):** [Code, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples show typed API requests, pagination, authentication setup, and decoded responses.]

## Skill Version(s):

0.15.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
