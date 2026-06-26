## Description: <br>
Stake and unstake INCLAWNCH tokens in the on-chain UBI staking contract on Base, and query treasury stats, wallet positions, APY estimates, and top stakers through public read endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stuart5915](https://clawhub.ai/user/stuart5915) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to prepare wallet-signed staking, unstaking, reward claiming, auto-compounding, and position-query workflows for INCLAWNCH on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signed transactions may approve or move INCLAWNCH balances if the chain, contract, function, spender, or amount is wrong. <br>
Mitigation: Before signing, verify the Base chain, token address, staking contract address, function selector, spender, and amount in the wallet. <br>
Risk: Wallet lookups and leaderboard data expose public financial and social identity information. <br>
Mitigation: Query and share wallet addresses, staking positions, and leaderboard data only with awareness that they are public and linkable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stuart5915/inclawnch-staking) <br>
- [INCLAWBATE Skills Directory](https://inclawbate.com/skills) <br>
- [Machine-Readable Staking Skill Spec](https://inclawbate.com/api/inclawbate/skill/staking) <br>
- [Public Staking Read Endpoint](https://inclawbate.com/api/inclawbate/staking) <br>
- [UBI Dashboard](https://inclawbate.com/ubi) <br>
- [BaseScan INCLAWNCH Token](https://basescan.org/token/0xB0b6e0E9da530f68D713cC03a813B506205aC808) <br>
- [BaseScan Staking Contract](https://basescan.org/address/0x206C97D4Ecf053561Bd2C714335aAef0eC1105e6) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline curl commands and transaction call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes public read API URLs and wallet-signed Base transaction details; no API key is required for reads.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
