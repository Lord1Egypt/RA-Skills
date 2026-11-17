## Description:

On-chain immutable data storage using IQ Labs tech stack (IQDB, hanLock, x402). Use when building Solana-based persistent storage, on-chain databases, tamper-evident records, password-encoded data, or paid file inscription. Triggers on tasks involving on-chain CRUD, Solana PDA storage, rolling hash verification, Hangul encoding, or HTTP 402 payment-gated inscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emanz1](https://clawhub.ai/user/emanz1)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Solana-backed persistent storage, tamper-evident records, password-obfuscated payloads, and payment-gated file inscription flows with IQDB, hanLock, and x402.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and payment actions can move real SOL or USDC and may be irreversible.

Mitigation: Start with a dedicated low-value devnet wallet, confirm the recipient, amount, token, network, and service identity before signing, and use mainnet only after testing.

Risk: Solana keypair JSON files are private keys and can authorize transactions if exposed.

Mitigation: Store keypair files outside shared project folders, restrict file permissions, and never commit or paste keypair contents.

Risk: On-chain storage is public and permanent, while hanLock is obfuscation rather than strong encryption.

Mitigation: Do not store secrets, private keys, passwords, or personal data on-chain; use proven encryption and off-chain storage for sensitive payloads.

Risk: Installer and dependency commands may fetch external packages or tooling.

Mitigation: Pin dependency versions, verify package names and installer sources, and review lockfiles before running generated setup commands.

Risk: IQDB row size limits, append-only writes, RPC rate limits, and x402 chunk failures can cause failed or incomplete writes.

Mitigation: Keep row JSON small, use status checks for inscriptions, add write delays or dedicated RPC providers, and design applications to apply correction history explicitly.

## Reference(s):

- [IQDB Skill Page](https://clawhub.ai/emanz1/skills/iqdb)
- [IQDB Core SDK Reference](references/iqdb-core.md)
- [Environment Setup](references/setup.md)
- [hanLock Encoding Reference](references/hanlock.md)
- [x402 Payment API Reference](references/x402-payments.md)
- [IQ Labs SDK](https://www.npmjs.com/package/@iqlabs-official/solana-sdk)
- [Legacy IQDB SDK](https://www.npmjs.com/package/@iqlabsteam/iqdb)
- [hanLock Package](https://www.npmjs.com/package/hanlock)
- [Solana Web3.js](https://www.npmjs.com/package/@solana/web3.js)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Solana wallet, RPC, dependency, payment, and on-chain storage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
