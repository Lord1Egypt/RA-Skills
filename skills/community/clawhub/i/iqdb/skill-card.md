## Description: <br>
Provides guidance for building Solana-based immutable storage with IQDB, hanLock, and x402, including on-chain CRUD, PDA storage, tamper-evident records, password-encoded data, and paid file inscription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Emanz1](https://clawhub.ai/user/Emanz1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Solana applications use this skill to set up IQDB, write and read immutable rows, encode short data with hanLock, and route larger paid inscriptions through x402. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Solana writes and x402 inscriptions can create permanent public blockchain records. <br>
Mitigation: Test on devnet first and do not place private keys, passwords, personal data, regulated data, or confidential files on-chain unless protected by well-reviewed client-side encryption. <br>
Risk: Mainnet operations require transaction signing, wallet funds, and explicit payment approval. <br>
Mitigation: Use a dedicated low-balance wallet, manually approve payments and mainnet writes, and verify installer and package sources before use. <br>
Risk: hanLock is lightweight obfuscation rather than strong encryption. <br>
Mitigation: Use hanLock only for short, low-sensitivity data and choose established encryption for secrets or sensitive records. <br>


## Reference(s): <br>
- [IQDB Core SDK Reference](artifact/references/iqdb-core.md) <br>
- [Environment Setup](artifact/references/setup.md) <br>
- [hanLock Encoding Reference](artifact/references/hanlock.md) <br>
- [x402 Payment API Reference](artifact/references/x402-payments.md) <br>
- [IQ Labs SDK](https://www.npmjs.com/package/@iqlabs-official/solana-sdk) <br>
- [@iqlabsteam/iqdb](https://www.npmjs.com/package/@iqlabsteam/iqdb) <br>
- [hanLock](https://www.npmjs.com/package/hanlock) <br>
- [Solana Web3.js](https://www.npmjs.com/package/@solana/web3.js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, TypeScript, bash, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Solana wallet, transaction signing, payment, and permanent on-chain storage safety guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
