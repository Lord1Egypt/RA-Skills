## Description:

Fetch MethodAlgo crypto market intelligence with methodalgo-cli for crypto news, trading signals, token unlocks, ETF flows, chart snapshots, economic calendar events, macro data, market-wide totals, and Binance public spot/futures data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[methodalgo](https://clawhub.ai/user/methodalgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route market-intelligence requests through MethodAlgo CLI commands, retrieve structured crypto, macro, signal, snapshot, and Binance market data, and summarize the results for analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed third-party npm CLI and MethodAlgo service access.

Mitigation: Install only from trusted MethodAlgo sources, pin or verify the methodalgo-cli version, and keep the CLI updated to the documented minimum version.

Risk: METHODALGO_API_KEY or persistent login credentials can be exposed on shared machines.

Mitigation: Scope the API key to MethodAlgo service use, avoid persistent login on shared systems, and prefer environment-based secrets management.

Risk: Market, macro, or upstream API requests may fail or return incomplete data.

Mitigation: Surface authentication, network, and upstream errors directly, and do not fabricate missing market or macro values.

## Reference(s):

- [MethodAlgo Market Intel Explorer source homepage](https://github.com/methodalgo/methodalgo-market-intel-explorer)
- [MethodAlgo CLI package](https://www.npmjs.com/package/methodalgo-cli)
- [ClawHub skill page](https://clawhub.ai/methodalgo/skills/methodalgo-market-intel-explorer)
- [Command Reference](references/command-reference.md)
- [Output Shape Catalog](references/output-shape-catalog.md)
- [JSON Output Samples](references/sample-output.md)
- [Signal Channels Detailed Reference](references/signal-channels.md)
- [AI Prompt Templates](references/ai-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented parsing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal service usage requires METHODALGO_API_KEY; Binance public market-data commands do not require a MethodAlgo or Binance API key.]

## Skill Version(s):

1.4.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
