## Description: <br>
Plan liquidity provision on PancakeSwap. Use when user says "add liquidity on pancakeswap", "provide liquidity", "LP on pancakeswap", "farm pancakeswap", or describes wanting to deposit tokens into liquidity pools without writing code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan PancakeSwap liquidity positions by resolving token pairs, checking pool and yield data, choosing position type, fee tier, and price range, and producing a reviewable PancakeSwap add-liquidity link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts PancakeSwap-related services and sends basic device and agent details during initialization. <br>
Mitigation: Install and run it only in environments where that external contact is acceptable. <br>
Risk: The skill has broader local tool permissions than the planner requires. <br>
Mitigation: Review requested tool permissions before deployment and restrict shell, browser-opening, and network access where your agent runtime supports it. <br>
Risk: Generated PancakeSwap links can be wrong or misleading if token, chain, fee tier, amount, or price-range data is incorrect. <br>
Mitigation: Independently verify every token address, chain, amount, fee tier, price range, and wallet prompt before using any generated link. <br>


## Reference(s): <br>
- [PancakeSwap AI repository](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [Data Providers Reference](references/data-providers.md) <br>
- [Position Types Reference](references/position-types.md) <br>
- [ClawHub listing](https://clawhub.ai/pcs-bot/pcs-lp-planner) <br>
- [Publisher profile](https://clawhub.ai/user/pcs-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and PancakeSwap deep-link URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning guidance and links for user review; it does not execute liquidity transactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
