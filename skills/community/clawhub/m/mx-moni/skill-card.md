## Description:

This skill helps an agent handle Eastmoney MX simulated A-share portfolio operations, including holdings, balances, orders, fills, simulated buy/sell/cancel actions, and simulated trading posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeluli7459-dev](https://clawhub.ai/user/zoeluli7459-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and operate an Eastmoney MX simulated A-share portfolio through an agent. It is limited to simulated trading practice and must not be used for real-money trading, investment advice, watchlist management, stock screening, news research, or quote-only requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change simulated account state through buy, sell, cancel, cancel-all, and post actions.

Mitigation: Require an explicit simulated-trading request and complete action details before running any mutating operation.

Risk: A custom MX_API_URL can direct API keys and simulated trading actions to an untrusted endpoint.

Mitigation: Use the default trusted HTTPS endpoint unless the replacement endpoint is explicitly trusted.

Risk: Saved output files may contain private simulated portfolio records.

Mitigation: Keep the output directory private and avoid sharing generated JSON or TXT files unless the user approves.

## Reference(s):

- [mx-moni API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, API Calls]

**Output Format:** [Formatted text summaries with saved JSON and TXT result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY; writes outputs to MX_OUTPUT_DIR or ~/.codex/skills-output/mx_data/output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
