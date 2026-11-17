## Description:

Build Python or JavaScript integrations for odds-api.net, with public API discovery, paginated snapshots, and streaming guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odds-api](https://clawhub.ai/user/odds-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build or repair Python and JavaScript integrations with the public odds-api.net API. It provides starter project files and guidance for discovery, paginated odds snapshots, and streaming updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshot output may not represent complete bookmaker coverage or freshness.

Mitigation: Follow all snapshot pages and retain completeness, excluded bookmaker, stale bookmaker, and freshness metadata before treating results as full coverage.

Risk: An authenticated API key could be exposed through client-side code or logs.

Mitigation: Keep the key in the server-side runtime, never place it in browser code or URLs, and use a dummy key for loopback tests.

## Reference(s):

- [Integration guide](artifact/references/integration.md)
- [Streaming guide](artifact/references/streaming.md)
- [odds-api.net API documentation](https://odds-api.net/docs)
- [Public OpenAPI schema](https://api.odds-api.net/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Python and JavaScript source files, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starter integrations are read-only; users provide their own runtime API key for authenticated requests.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
