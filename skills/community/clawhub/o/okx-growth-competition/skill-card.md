## Description: <br>
Agentic Wallet exclusive trading competitions. Full lifecycle: discover, view rules, join, trade, check rank, and claim rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with an Agentic Wallet use this skill to discover OKX trading competitions, review rules and prize pools, register, check status and rankings, and claim eligible on-chain rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Join, trade, and claim flows can submit irreversible blockchain transactions from a logged-in wallet. <br>
Mitigation: Confirm the active wallet account, competition name, token contract, chain, amount, gas cost, and transaction intent before proceeding. <br>
Risk: Reward claims and trades can fail because of eligibility, expired claim windows, insufficient gas, simulation errors, or network issues. <br>
Mitigation: Check competition status before claiming, surface pre-check rejections without retrying, and only retry transient failures after the user reviews the failure details. <br>
Risk: Exporting a wallet that is registered for a competition can affect eligibility. <br>
Mitigation: Check competition user status before wallet export and continue only after the user explicitly confirms they understand the eligibility impact. <br>


## Reference(s): <br>
- [competition CLI Reference](references/cli-reference.md) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX Trading Competition Page](https://web3.okx.com/boost/trading-competition/{shortName}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown responses with tables, fixed status templates, transaction hashes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate wallet-backed competition join, trade delegation, and reward claim flows when the user confirms the relevant action.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
