## Description:

Writes Go code with go-bunnynet (package bunnynet, github.com/psyb0t/go-bunnynet), an unofficial generated client for the Bunny.net core API covering CDN pull zones, cache purges, DNS, storage and video library configuration, statistics, load balancers and billing. Use when a Go project imports go-bunnynet or needs Bunny.net core API calls. Excludes storage file transfers and the separate Stream API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Bunny.net core API integrations to Go projects with the unofficial go-bunnynet client, including CDN, DNS, storage and video library configuration, statistics, load balancers, and billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bunny.net account API key can authorize account requests.

Mitigation: Keep the key private in the environment; do not hardcode or log it.

Risk: Creating, changing, deleting, purging, rotating keys, or closing accounts can affect the user's account.

Mitigation: Request specific account changes deliberately and confirm the intended operation before applying it.

Risk: This is an unofficial integration, and the security assessment covers the bundled instructions rather than a full audit of downloaded dependency code.

Mitigation: Review and pin the dependency version before use.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-bunnynet package documentation](https://pkg.go.dev/github.com/psyb0t/go-bunnynet)
- [go-bunnynet project homepage](https://github.com/psyb0t/go-bunnynet)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-bunnynet)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and integration guidance vary with the requested Bunny.net core API operation.]

## Skill Version(s):

0.4.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
