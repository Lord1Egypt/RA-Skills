## Description: <br>
Integrate HashPack wallet for Hedera blockchain authentication, including login, HBAR transaction signing, DApp connection, and account balance retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to add HashPack wallet authentication and Hedera transaction workflows to web applications. It helps agents provide integration guidance for connecting, disconnecting, signing transactions, querying balances, and choosing Hedera network endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet transaction guidance can lead to unintended transfers if transaction details are unclear. <br>
Mitigation: Require user confirmation before every signature and show the network, recipient, amount, and fees before signing. <br>
Risk: Production wallet flows may be deployed before transaction behavior is fully tested. <br>
Mitigation: Test integrations on Hedera testnet before enabling mainnet use. <br>
Risk: Users could be prompted for sensitive wallet secrets during integration work. <br>
Mitigation: Never ask users for seed phrases or private keys. <br>


## Reference(s): <br>
- [HashPack Wallet Skill on ClawHub](https://clawhub.ai/HarleysCodes/hashpack-wallet) <br>
- [Publisher Profile](https://clawhub.ai/user/HarleysCodes) <br>
- [Hashio Mainnet API](https://mainnet.hashio.io/api) <br>
- [Hashio Testnet API](https://testnet.hashio.io/api) <br>
- [Hashio Previewnet API](https://previewnet.hashio.io/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
