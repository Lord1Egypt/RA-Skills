## Description:

IQDB On-Chain Storage guides agents in building Solana-based persistent storage, on-chain databases, tamper-evident records, password-encoded data, and paid file inscription workflows using IQDB, hanLock, and x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emanz1](https://clawhub.ai/user/emanz1)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Solana-backed applications that need persistent structured data, tamper-evident records, lightweight data obfuscation, or payment-gated file inscription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-chain data and inscriptions are permanent and may be public.

Mitigation: Do not store secrets, keys, credentials, PII, regulated records, or private documents unless strong client-side encryption is applied and the user accepts the permanence risk.

Risk: Wallet-backed payments and Solana writes can move funds or publish irreversible transaction data.

Mitigation: Require explicit user review of recipient, amount, network, payment token, file metadata, and transaction intent before signing.

Risk: Setup steps include installer and dependency commands that can change the user's local environment.

Mitigation: Verify the Solana installer source before execution, pin package versions, and prefer a controlled development environment.

Risk: hanLock provides lightweight obfuscation rather than cryptographic protection.

Mitigation: Use strong encryption for sensitive data and treat hanLock output as unsuitable for protecting secrets against determined attackers.

## Reference(s):

- [IQDB Core SDK Reference](artifact/references/iqdb-core.md)
- [hanLock Encoding Reference](artifact/references/hanlock.md)
- [Environment Setup](artifact/references/setup.md)
- [x402 Payment API Reference](artifact/references/x402-payments.md)
- [IQ Labs SDK](https://www.npmjs.com/package/@iqlabs-official/solana-sdk)
- [@iqlabsteam/iqdb](https://www.npmjs.com/package/@iqlabsteam/iqdb)
- [hanLock](https://www.npmjs.com/package/hanlock)
- [Solana Web3.js](https://www.npmjs.com/package/@solana/web3.js)
- [ClawHub Skill Page](https://clawhub.ai/emanz1/skills/iqdb-onchain-storage)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet, RPC, dependency, transaction-signing, and data-size constraints for Solana workflows.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
