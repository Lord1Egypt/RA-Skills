## Description: <br>
Plan yield farming, CAKE staking, and reward harvesting on PancakeSwap by discovering active farms, comparing APR/APY, and generating deep links to the PancakeSwap farming interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi users and agent operators use this skill to discover PancakeSwap farm and Syrup Pool opportunities, compare APR/APY, inspect wallet positions, and prepare UI deep links or shell commands for user-reviewed staking, unstaking, and harvesting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes mainnet transaction guidance that can lead to real on-chain actions. <br>
Mitigation: Review every transaction section before use and do not run any cast send command or token approval unless the user deliberately intends that action. <br>
Risk: Helper scripts may install Python packages at runtime. <br>
Mitigation: Avoid running helper scripts until dependencies are pinned and installed through a reviewed setup process. <br>
Risk: Wallet-position inspection exposes sensitive operational context for DeFi users. <br>
Mitigation: Use only intended public wallet addresses and treat returned balances, positions, and pending rewards as user-sensitive information. <br>


## Reference(s): <br>
- [ClawHub Farming Planner release](https://clawhub.ai/pcs-bot/pcs-farming-planner) <br>
- [Publisher profile: pcs-bot](https://clawhub.ai/user/pcs-bot) <br>
- [PancakeSwap AI repository](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [fetch-farms.py](artifact/references/fetch-farms.py) <br>
- [fetch-solana.cjs](artifact/references/fetch-solana.cjs) <br>
- [fetch-syrup-pools.py](artifact/references/fetch-syrup-pools.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, deep links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PancakeSwap deep links and user-reviewed cast examples; the skill states that it does not execute transactions itself.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
