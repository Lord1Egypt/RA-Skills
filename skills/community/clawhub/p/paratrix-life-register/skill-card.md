## Description: <br>
Automates Paratrix Life registration and Soulbound Token minting on the Karpak Living Map through a local browser-wallet bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karpak-developer](https://clawhub.ai/user/karpak-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register a wallet profile with Paratrix Life and mint a Karpak Living Map SBT. It is intended for wallet-mediated registration flows where the user can review each wallet signature and transaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate wallet signatures and blockchain transactions, including on mainnet. <br>
Mitigation: Explicitly choose testnet or mainnet, verify the wallet popup chain ID and contract, and use a wallet with limited funds. <br>
Risk: Bundled local agent permission files grant broad command and wallet-automation authority. <br>
Mitigation: Review or remove bundled .claude permission files before enabling the skill in an agent workspace. <br>
Risk: Security evidence marks the release as suspicious because behavior can differ from testnet-default documentation. <br>
Mitigation: Confirm the selected environment before execution and require user approval for every signature and transaction prompt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/karpak-developer/paratrix-life-register) <br>
- [Publisher profile](https://clawhub.ai/user/karpak-developer) <br>
- [Karpak Life API](https://lifestyle-api.karpak.xyz) <br>
- [Paratrix SBT service](https://sbt.karpak.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, status summaries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, a compatible Web3 wallet, BNB for gas, and user confirmation for wallet signatures and transactions.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
