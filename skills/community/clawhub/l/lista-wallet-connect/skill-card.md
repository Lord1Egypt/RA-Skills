## Description: <br>
Connect wallets via WalletConnect v2 and execute EVM signing/contract-call operations on Ethereum and BSC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lawson-ccy](https://clawhub.ai/user/lawson-ccy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working with Lista or EVM workflows use this skill to pair a WalletConnect wallet, request signatures, and submit simulated Ethereum or BSC contract transactions after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate wallet signature requests and EVM transactions that may authorize actions or move assets. <br>
Mitigation: Require explicit user review and wallet approval, use a limited-purpose wallet, keep transaction simulation enabled by default, and avoid --no-simulate unless the user understands the transaction. <br>
Risk: WalletConnect sessions and wallet metadata are stored locally under ~/.agent-wallet. <br>
Mitigation: Periodically delete saved sessions that are no longer needed and avoid using high-value wallets for routine agent workflows. <br>
Risk: Debug logs and a shared WalletConnect project ID can expose transaction or session context. <br>
Mitigation: Avoid debug logging for real transactions and override WALLETCONNECT_PROJECT_ID when privacy matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lawson-ccy/lista-wallet-connect) <br>
- [Supported Chains & Tokens](references/chains.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON status payloads with concise human-facing summaries and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet-request commands may stream an interim waiting_for_approval event before a terminal status.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter and package.json declare 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
