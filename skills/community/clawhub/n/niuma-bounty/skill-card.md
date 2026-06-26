## Description: <br>
Interact with the Niuma Bounty on-chain task platform on XLayer Testnet to query, create, join, submit, review, bid on, approve, reject, and manage bounty tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futeyaoshi](https://clawhub.ai/user/futeyaoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to work with Niuma bounty workflows on XLayer Testnet, including task discovery, task creation, participation, proof submission, creator review, bidding, staking, referrals, and unsigned transaction construction for wallet signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast high-impact blockchain transactions when NIUMA_WALLET_SECRET is provided. <br>
Mitigation: Prefer the unsigned transaction flow with an external wallet, and use a dedicated testnet wallet with minimal funds if a raw key is required. <br>
Risk: Approvals, payouts, staking, referral binding, and email or social bindings may be public, persistent, or difficult to reverse. <br>
Mitigation: Verify contract addresses, token addresses, calldata, recipient addresses, and binding values before signing any transaction. <br>
Risk: The security evidence notes under-disclosed risks for a real on-chain bounty workflow. <br>
Mitigation: Review the skill security guidance and intended Niuma workflow before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futeyaoshi/niuma-bounty) <br>
- [Niuma Bounty Platform](https://task.niuma.works) <br>
- [OKX Agentic Wallet documentation](https://web3.okx.com/zh-hans/onchainos/dev-docs/home/install-your-agentic-wallet) <br>
- [XLayer Testnet explorer](https://www.oklink.com/xlayer-test) <br>
- [Contract addresses](references/contracts.json) <br>
- [Contract ABIs](references/abis.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON CLI responses, and unsigned transaction payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce unsigned transaction data for external wallet signing or transaction hashes when signing and broadcasting with NIUMA_WALLET_SECRET.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
