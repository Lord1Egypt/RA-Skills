## Description:

Use this skill when a task needs IEX Cloud market data through the REST API (quotes, charts, fundamentals, market lists, and batch calls), including secure token handling and scriptable CLI usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to select IEX Cloud market-data endpoints, configure token-based access, and run repeatable quote, chart, fundamentals, market-list, news, batch, or raw API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing an API token with --token can expose it through shell history or local process inspection.

Mitigation: Prefer OpenClaw SecretRefs or IEX_TOKEN/IEX_CLOUD_TOKEN environment injection, and avoid placing production tokens directly on the command line.

Risk: The skill makes authenticated market-data requests, so misuse can consume IEX Cloud quota or return provider-side errors for invalid symbols, plans, or parameters.

Mitigation: Use sandbox configuration for testing, keep curl timeouts bounded, validate inputs before calls, and review non-2xx or API-level error responses before downstream use.

## Reference(s):

- [IEX Cloud API Reference](references/api_docs.md)
- [IEX Cloud API Docs](https://iexcloud.io/docs/api/)
- [IEX API Status](https://status.iexapis.com/)
- [OpenClaw Secrets](https://docs.openclaw.ai/gateway/secrets)
- [Skill Homepage](https://github.com/oscraters/iex-cloud-skill)
- [ClawHub Skill Page](https://clawhub.ai/oscraters/skills/iex-cloud)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with bash commands and JSON or raw API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an IEX Cloud token through IEX_TOKEN, IEX_CLOUD_TOKEN, OpenClaw SecretRefs, or an explicit CLI token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
