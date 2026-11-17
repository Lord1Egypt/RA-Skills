## Description:

Query Nasdaq public market APIs from scripts or agent workflows for stock screener pulls, symbol lists, paginated screener rows, and guidance grounded in Nasdaq Data Link public API docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch Nasdaq public screener stock data with pagination and to ground Nasdaq Data Link API decisions in bundled official references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to Nasdaq when invoked.

Mitigation: Install and use it only when outbound Nasdaq requests are acceptable for the deployment environment.

Risk: The public screener endpoint is operational web behavior and may change.

Mitigation: Review Nasdaq terms and rate limits for the use case, pace requests, and validate response shape before downstream processing.

## Reference(s):

- [Nasdaq API References](references/api_docs.md)
- [Nasdaq Data Organization](https://docs.data.nasdaq.com/docs/data-organization)
- [Nasdaq Real-Time/Delayed REST API Rate Limits](https://docs.data.nasdaq.com/docs/rate-limits-for-real-timedelayed-rest-api)
- [Nasdaq Data Link API](https://www.nasdaq.com/solutions/data/nasdaq-data-link/api)
- [ClawHub Skill Page](https://clawhub.ai/oscraters/skills/nasdaq-public)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output can be raw JSON, compact row JSON, or newline-delimited ticker symbols.]

## Skill Version(s):

1.0.0 (source: server evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
