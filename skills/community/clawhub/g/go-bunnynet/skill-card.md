## Description:

Writes Go code with go-bunnynet (package bunnynet, github.com/psyb0t/go-bunnynet), an unofficial generated client for the Bunny.net core API covering CDN pull zones, cache purges, DNS, storage and video library configuration, statistics, load balancers and billing. Use when a Go project imports go-bunnynet or needs Bunny.net core API calls. Excludes storage file transfers and the separate Stream API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go code that configures and queries Bunny.net core services through the unofficial go-bunnynet client. It guides dependency setup, authentication, endpoint and response handling, and account-impacting operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign with medium confidence, but two local references were unmatched, leaving some evidence incomplete.

Mitigation: Review the referenced material and consider the scan's stated limitation when deciding whether to install.

Risk: Using the client can affect the user's Bunny.net account, including creating or deleting resources, purging caches, rotating keys, or closing accounts.

Mitigation: Use the API key from the environment, never hardcode or log credentials, and perform account-changing operations only when requested.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [GitHub repository](https://github.com/psyb0t/go-bunnynet)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-bunnynet)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and API usage guidance; the library reads and writes no files.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
