## Description:

Unofficial Go client for the Twelve Data market data API, generated with oapi-codegen, providing typed REST methods for prices, quotes, time series, technical indicators, fundamentals, instrument metadata and batch queries when Go code needs Twelve Data market data or already imports go-twelvedata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate the unofficial, typed Twelve Data client into a project and make market data requests. It guides installation, authentication, endpoint and response handling, and request limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API key placed in a URL query parameter can appear in URL logs.

Mitigation: Read the key from TWELVEDATA_API_KEY, send it in the Authorization header, and do not hardcode, commit, or log credentials or authenticated requests.

Risk: Requests, including constituent requests in a batch, consume API credits and may be subject to plan permissions and rate limits.

Mitigation: Check the user's plan and data permissions, monitor usage, and handle HTTP 429 responses with bounded backoff and a caller deadline.

Risk: The security review was partial because two referenced paths were missing, so its benign verdict has medium confidence.

Mitigation: Review the complete skill and its referenced files before deployment; do not treat the scanner verdict as a guarantee of safety.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-twelvedata)
- [Project homepage](https://github.com/psyb0t/go-twelvedata)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-twelvedata)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.7.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
