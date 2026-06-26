## Description: <br>
Read-only API reference for NexusWeb3 safety protocols 21-30 on Base mainnet, including kill switch status, KYA verification, audit logs, bounties, licensing, milestones, subscriptions, insolvency, referrals, and collectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexusweb3dev](https://clawhub.ai/user/nexusweb3dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to look up NexusWeb3 safety and compliance protocol addresses, view functions, and call examples for Base mainnet. It is best used as a reference before querying on-chain state or reviewing transaction proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes examples for irreversible or value-moving blockchain actions such as approvals, bounties, kill switches, insolvency flows, and treasury movement. <br>
Mitigation: Use the skill as a reference only unless a trusted wallet-signing setup is intentionally configured and the exact transaction, fees, permanence, and privacy impact are reviewed first. <br>
Risk: Agents may confuse read-only reference material with authorization to submit transactions. <br>
Mitigation: Restrict automated use to view functions and require explicit human review before any write operation or token approval. <br>
Risk: On-chain state and contract behavior can affect funds, compliance status, and public records. <br>
Mitigation: Verify current contract state, target addresses, and transaction parameters on Base mainnet before relying on results or signing calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nexusweb3dev/nexusweb3-safety) <br>
- [Publisher Profile](https://clawhub.ai/user/nexusweb3dev) <br>
- [NexusWeb3 Protocols Repository](https://github.com/nexusweb3dev/nexusweb3-protocols) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [BaseScan](https://basescan.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown reference with contract addresses, Solidity function signatures, and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reference; no executable code, credentials, persistence, or automatic wallet access.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
