## Description: <br>
Place, manage, and cancel orders using REST API or SDK hooks. Covers market, limit, IOC, FOK, POST_ONLY order types and batch operations <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add Orderly Network order placement, validation, editing, cancellation, batch order handling, and order monitoring to trading interfaces or automated trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill teaches live financial order placement and broad cancellation flows that could cause unintended trades or cancellations. <br>
Mitigation: Require manual confirmation for every live order, use a sandbox or limited account first, and prefer symbol-scoped cancellation. <br>
Risk: Trading API keys could grant more authority than the workflow needs. <br>
Mitigation: Keep trading keys tightly scoped, protect private keys, and avoid using unrestricted production credentials during testing. <br>
Risk: Batch or automated examples can amplify order size and notional exposure. <br>
Mitigation: Set external order size, notional, and account limits before using batch or automated order workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Tarnadas/orderly-trading-orders) <br>
- [Orderly Place Order Endpoint](https://api.orderly.org/v1/order) <br>
- [Orderly Symbol Info Endpoint](https://api.orderly.org/v1/public/info/PERP_ETH_USDC) <br>
- [Orderly Batch Order Endpoint](https://api.orderly.org/v1/batch-order) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, REST API, and React SDK examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before use with live trading accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
