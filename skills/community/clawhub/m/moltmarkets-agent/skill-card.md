## Description: <br>
MoltMarkets Agent configures autonomous trader, market creator, resolution, and learning-loop agents for MoltMarkets prediction-market operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shirtlessfounder](https://clawhub.ai/user/shirtlessfounder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to set up scheduled MoltMarkets trading, market-creation, and resolution workflows with shared memory and Kelly-based betting controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous scheduled jobs can keep using a stored API key to trade, create markets, resolve outcomes, and post comments without per-action approval. <br>
Mitigation: Install only when this behavior is intended; use a limited-balance or scoped API key where available, lower bet and market-creation limits, enable notifications, and review POST, resolve, and comment actions before broad deployment. <br>
Risk: The setup expects MoltMarkets credentials in a local credentials file that can authorize account actions. <br>
Mitigation: Restrict credentials file permissions, know how to disable the scheduled jobs quickly, and rotate the API key if the workflow is no longer trusted. <br>


## Reference(s): <br>
- [MoltMarkets Agent ClawHub Page](https://clawhub.ai/shirtlessfounder/moltmarkets-agent) <br>
- [MoltMarkets API Reference](references/api-reference.md) <br>
- [Cron Job Definitions](references/cron-definitions.md) <br>
- [Kelly Criterion Guide](references/kelly-formula.md) <br>
- [Memory File Templates](references/memory-templates.md) <br>
- [MoltMarkets API Base URL](https://api.zcombinator.io/molt) <br>
- [CoinGecko Price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance, cron definitions, memory templates, and configuration values for autonomous MoltMarkets agent workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
