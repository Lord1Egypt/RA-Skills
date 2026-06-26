## Description: <br>
Hypii Hyperliquid Trader helps agents query Hyperliquid portfolio and market data, generate DCA, grid, and signal outputs, and submit Hyperliquid perpetual futures trades when configured with trading credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JarviYin](https://clawhub.ai/user/JarviYin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to automate Hyperliquid portfolio checks, price lookups, strategy planning, signal generation, and optional live trade execution through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill can place live crypto trades and ships exposed trading-key material in runnable scripts. <br>
Mitigation: Do not use it with real funds until exposed keys are removed, affected keys are rotated, runnable live-trade demos are deleted or isolated, and dry-run or testnet mode is the default. <br>
Risk: The security guidance calls for stronger live-trade controls before use. <br>
Mitigation: Require an order preview and explicit confirmation for every live trade, validate trade side and order parameters, and keep private keys only in secret-managed environment variables. <br>
Risk: Artifact behavior includes randomized signal generation that can appear to be trading analysis. <br>
Mitigation: Clearly label randomized signals as non-advisory examples or replace them with documented analysis logic before presenting them as trading guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JarviYin/hypii-hyperliquid-trader) <br>
- [x402 protocol](https://www.x402.org/) <br>
- [Base network](https://base.org) <br>
- [USDC developer documentation](https://www.circle.com/en/usdc/developers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Agent responses with structured JSON data, human-readable status text, and command/configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return payment-required responses, portfolio and price data, strategy plans, signal summaries, and trade execution status.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, skill.yaml, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
