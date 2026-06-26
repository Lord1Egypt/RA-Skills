## Description: <br>
On-chain immutable data storage using IQ Labs tech stack (IQDB, hanLock, x402). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Emanz1](https://clawhub.ai/user/Emanz1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build Solana-backed persistent storage, tamper-evident records, password-encoded data, and payment-gated file inscription workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet signing, mainnet transactions, and x402 payments can move real assets. <br>
Mitigation: Start on devnet or with a low-balance wallet, protect the ANCHOR_WALLET keypair, and verify every mainnet transaction or payment before signing. <br>
Risk: On-chain storage and file inscription are public and permanent. <br>
Mitigation: Do not store secrets, private keys, personal data, regulated data, or unencrypted confidential files on-chain. <br>
Risk: hanLock provides lightweight obfuscation rather than strong encryption. <br>
Mitigation: Use proper encryption for sensitive data and keep hanLock payloads short enough for IQDB row size limits. <br>
Risk: RPC rate limits and Solana transaction size constraints can cause failed writes. <br>
Mitigation: Use a dedicated RPC provider for production, add delays between rapid writes, and split larger payloads across rows or inscription chunks. <br>


## Reference(s): <br>
- [IQDB Core SDK Reference](references/iqdb-core.md) <br>
- [Environment Setup](references/setup.md) <br>
- [hanLock Encoding Reference](references/hanlock.md) <br>
- [x402 Payment API Reference](references/x402-payments.md) <br>
- [IQ Labs SDK](https://www.npmjs.com/package/@iqlabs-official/solana-sdk) <br>
- [@iqlabsteam/iqdb](https://www.npmjs.com/package/@iqlabsteam/iqdb) <br>
- [hanLock](https://www.npmjs.com/package/hanlock) <br>
- [Solana Web3.js](https://www.npmjs.com/package/@solana/web3.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline JavaScript, TypeScript, shell, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Solana setup guidance, SDK usage examples, API request examples, and operational constraints.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
