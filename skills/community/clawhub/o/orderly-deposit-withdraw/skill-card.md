## Description: <br>
Handle token deposits and withdrawals across chains, including allowance approval, vault interactions, and cross-chain operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Orderly Network deposit, withdrawal, and internal-transfer flows use this skill for React SDK examples, REST API request patterns, token approval handling, and EVM or Solana signing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples describe deposits, withdrawals, internal transfers, token approvals, and signatures that can move real assets. <br>
Mitigation: Require human confirmation for every destination, chain, token, amount, and environment before executing any transaction or API request. <br>
Risk: Unlimited token approvals can expose funds if the spender address or integration is wrong or later compromised. <br>
Mitigation: Avoid unlimited approvals unless explicitly accepted, verify vault and token addresses from official Orderly sources, and revoke unused allowances. <br>
Risk: Frontend or log exposure of private keys, Ed25519 API signing material, or wallet signatures can compromise accounts. <br>
Mitigation: Keep private keys and API signing material out of frontend code and logs, and use official Orderly authentication guidance for signing. <br>
Risk: Incorrect contract, chain, token, collateral, or fee data can cause failed transactions or asset loss. <br>
Mitigation: Fetch chain, token, contract, collateral, nonce, and fee data from official Orderly sources at runtime rather than relying on copied examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tarnadas/orderly-deposit-withdraw) <br>
- [Orderly EVM testnet faucet endpoint](https://testnet-operator-evm.orderly.org/v1/faucet/usdc) <br>
- [Orderly Solana testnet faucet endpoint](https://testnet-operator-sol.orderly.org/v1/faucet/usdc) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown with TypeScript code blocks, API endpoint examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for wallet-signed crypto asset movement; examples require human review before use with real funds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
