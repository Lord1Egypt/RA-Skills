## Description: <br>
Guides users through native Solana limit orders with `nansen trade limit-order` and alert-based settlement signals for chains without native support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare or run Nansen CLI commands for creating, listing, canceling, and updating Solana limit orders, or to configure settlement-signal alerts on other chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent assistance can affect real wallet-backed crypto orders. <br>
Mitigation: Confirm wallet, token pair, side, amount, trigger price, slippage, expiry, and order ID before create, cancel, or update commands. <br>
Risk: API keys, wallet configuration, alert metadata, and the temporary Nansen JWT are sensitive. <br>
Mitigation: Use private notification channels or dedicated webhooks, avoid shared machines, and protect NANSEN_API_KEY and ~/.nansen/limit-order-auth.json. <br>
Risk: Alert-based fallback signals are not authoritative order tracking for non-Solana chains. <br>
Mitigation: Treat alerts as best-effort settlement signals and verify fills with the trading venue or on-chain records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-limit-orders) <br>
- [Nansen CLI npm package](https://www.npmjs.com/package/nansen-cli) <br>
- [Nansen CLI GitHub repository](https://github.com/nansen-ai/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Nansen CLI commands requiring NANSEN_API_KEY and wallet configuration; users should verify trade details before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
