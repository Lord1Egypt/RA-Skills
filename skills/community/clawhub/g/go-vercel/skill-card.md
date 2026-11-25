## Description:

Provides a typed Go client for calling Vercel's REST API, including projects, deployments, domains, DNS, environment variables, and teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the Go client to call Vercel API endpoints from Go applications, with typed parameters and responses. It supports account and team workflows for projects, deployments, domains, DNS, environment variables, and related resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Vercel bearer token can grant access to account or team resources.

Mitigation: Read the token from an environment variable, keep it out of source control and logs, and confirm the intended account or team.

Risk: Some API operations can change or delete live resources.

Mitigation: Run only operations the user requested and review the target resources and parameters before sending a request.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-vercel)
- [Project homepage](https://github.com/psyb0t/go-vercel)

## Skill Output:

**Output Type(s):** [Code, API Calls, Configuration instructions, Shell commands]

**Output Format:** [Markdown with Go code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typed request and response examples; requires user-supplied endpoint parameters and Vercel credentials.]

## Skill Version(s):

0.36.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
