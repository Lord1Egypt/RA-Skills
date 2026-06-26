## Description: <br>
Trade prediction markets non-custodially via the official KashDAO CLI (@kashdao/cli) with market browsing, quotes, buy/sell trades, idempotency, high-value confirmation, portfolio management, webhooks, and request tracing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwhdx](https://clawhub.ai/user/bwhdx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to operate the KashDAO CLI for prediction-market workflows, including market discovery, quoting, trading, portfolio inspection, webhook management, and request tracing. It supports both Kash-orchestrated REST API flows and self-orchestrated direct-to-chain protocol flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with access to KASH_API_KEY can initiate trading workflows that may affect user funds or positions. <br>
Mitigation: Use test keys where possible, scope and revoke keys appropriately, review trade amounts before execution, and require high-value confirmation for large trades. <br>
Risk: Using @kashdao/cli@latest may install a newer package than the version reviewed here. <br>
Mitigation: Pin a specific npm package version for controlled deployments. <br>
Risk: Retrying trade write paths without idempotency could duplicate intended actions. <br>
Mitigation: Use the documented --auto-idempotency-key behavior for agent trade flows. <br>


## Reference(s): <br>
- [KashDAO CLI GitHub repository](https://github.com/KashDAO/cli) <br>
- [Kash CLI documentation](https://docs.kash.bot/developer-docs/cli) <br>
- [Kash REST API overview](https://docs.kash.bot/developer-docs/rest-api/overview) <br>
- [Kash API error catalog](https://docs.kash.bot/developer-docs/api-errors) <br>
- [Non-custodial design statement](https://github.com/KashDAO/cli/blob/main/SECURITY.md#non-custodial-design) <br>
- [npm package @kashdao/cli](https://www.npmjs.com/package/@kashdao/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends stable JSON CLI output for agent workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
