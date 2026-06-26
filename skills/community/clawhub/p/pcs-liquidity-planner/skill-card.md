## Description: <br>
Plans PancakeSwap liquidity positions by gathering intent, resolving and verifying tokens, assessing pool metrics, recommending price ranges and fee tiers, and generating a reviewable add-liquidity link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi users and agents use this skill to plan PancakeSwap liquidity provision without writing code, compare pool choices and risk tradeoffs, and generate a deep link for user review in the PancakeSwap interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts pancakeswap.ai during invocation. <br>
Mitigation: Install and use it only where that network contact is acceptable. <br>
Risk: The skill requests broad local command and browser-opening permissions. <br>
Mitigation: Review proposed commands and browser actions before allowing them, especially when local tools or URLs are involved. <br>
Risk: Generated PancakeSwap links are transaction-adjacent and can lead to wallet approvals or liquidity actions. <br>
Mitigation: Before using any link, manually verify the chain, token addresses, pool type, fee tier, amounts, wallet prompts, approvals, and Infinity auto-farming behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pcs-bot/pcs-liquidity-planner) <br>
- [ClawDIS Homepage](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [Data Providers Reference](references/data-providers.md) <br>
- [Position Types Reference](references/position-types.md) <br>
- [PancakeSwap Interface](https://pancakeswap.finance/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown plan with tables, warnings, command snippets, and a PancakeSwap deep link URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute transactions; generated links require manual user review and wallet confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
