## Description:

Uses a local Python wrapper to call the official iFinD QuantAPI HTTP endpoints for market, macro, fund, code-conversion, calendar, report, and portfolio data while checking refresh-token setup before requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yannlong](https://clawhub.ai/user/yannlong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to make authenticated iFinD QuantAPI HTTP requests through bundled Python scripts for market, macro, fund, code-conversion, calendar, report, and portfolio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently handles a long-lived iFinD account refresh token.

Mitigation: Use a dedicated low-scope token when possible, avoid passing the token on the command line, and verify credential file permissions before use.

Risk: The skill can make broad authenticated QuantAPI calls, including generic endpoint calls.

Mitigation: Review the requested endpoint, payload, symbol universe, and date range before allowing calls, especially when using generic endpoint mode.

Risk: Authenticated API results may be used in downstream analysis without sufficient context.

Mitigation: Report the endpoint, code list, requested date range or timestamp, and returned API metadata such as perf or dataVol when using results.

## Reference(s):

- [iFinD API Reference](references/iFind_API_Reference.md)
- [refresh_token acquisition and storage](references/token-and-storage.md)
- [iFinD QuantAPI](https://quantapi.51ifind.com)
- [iFinD QuantAPI v1 endpoint base](https://quantapi.51ifind.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python usage, configuration steps, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an iFinD refresh_token and network access to quantapi.51ifind.com.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
