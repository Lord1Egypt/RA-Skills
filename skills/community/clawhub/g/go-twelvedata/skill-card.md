## Description:

Provides Go developers with an unofficial, typed Twelve Data API client for prices, quotes, time series, technical indicators, fundamentals, instrument metadata, and batch queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to add typed Twelve Data API calls for market prices, time series, technical indicators, company fundamentals, instrument metadata, and batch requests. It guides installation, authentication, endpoint and type lookup, response handling, and use within API access and credit limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and two local file references could not be resolved, leaving some evidence incomplete.

Mitigation: Review whether those referenced files are relevant before installation; the scan does not establish that the skill is risk-free.

Risk: An API key placed in a query parameter or included in logs could be exposed.

Mitigation: Read the key from TWELVEDATA_API_KEY, send it in the Authorization header, and never hardcode, commit, or log the key or authenticated request.

Risk: Requests consume API credits, and access depends on the user's plan and data permissions.

Mitigation: Respect the user's plan, data permissions, and request budget; use bounded backoff and a caller deadline when handling HTTP 429 responses.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/psyb0t/skills/go-twelvedata)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-twelvedata)
- [Setup and reference](references/setup.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and instructions for integrating the Go client; no files are produced by the library itself.]

## Skill Version(s):

0.5.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
