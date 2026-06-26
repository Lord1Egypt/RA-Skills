## Description: <br>
Fetch MethodAlgo crypto market intelligence with methodalgo-cli for crypto news, trading signals, token unlocks, ETF flows, chart snapshots, economic calendar events, macro data, market totals, and Binance public spot and futures data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[methodalgo](https://clawhub.ai/user/methodalgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market analysts use this skill to route crypto market-intelligence requests through MethodAlgo CLI commands and receive structured data for news, signals, macro indicators, market totals, chart snapshots, and public Binance market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MethodAlgo API key for normal service usage. <br>
Mitigation: Store METHODALGO_API_KEY in an environment variable or secret manager, avoid exposing it in prompts or logs, and rotate the key if it is disclosed. <br>
Risk: Market queries, symbols, search terms, and request parameters may be sent to MethodAlgo and Binance public endpoints. <br>
Mitigation: Avoid including proprietary trading strategy details or other sensitive information in prompts, search strings, and command parameters. <br>
Risk: The workflow uses a globally installed npm CLI. <br>
Mitigation: Install the disclosed methodalgo-cli package from a trusted source, keep it updated to the documented minimum version, and review generated commands before execution. <br>


## Reference(s): <br>
- [MethodAlgo Market Intel Explorer on ClawHub](https://clawhub.ai/methodalgo/methodalgo-market-intel-explorer) <br>
- [Project Homepage](https://github.com/methodalgo/methodalgo-market-intel-explorer) <br>
- [methodalgo-cli Package](https://www.npmjs.com/package/methodalgo-cli) <br>
- [Command Reference](references/command-reference.md) <br>
- [Signal Channels](references/signal-channels.md) <br>
- [Output Shape Catalog](references/output-shape-catalog.md) <br>
- [Sample Output](references/sample-output.md) <br>
- [AI Prompt Templates](references/ai-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-oriented CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to request JSON output from methodalgo-cli and to surface authentication, version, or upstream data errors explicitly.] <br>

## Skill Version(s): <br>
1.4.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
