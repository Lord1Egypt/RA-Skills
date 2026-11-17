## Description:

Install and run Lightning Terminal (litd) which bundles lnd, loop, pool, tapd, and faraday in a single Docker container. Defaults to neutrino backend with SQLite storage on testnet. Supports watch-only mode with remote signer, standalone mode, and regtest development. Use when setting up a Lightning node for payments, channel management, liquidity management (loop), channel marketplace (pool), taproot assets (tapd), or enabling agent L402 commerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, configure, and run Lightning Terminal/LND nodes for payments, channel management, liquidity operations, taproot assets, and L402 commerce. It supports Docker and native workflows across testnet, signet, regtest, watch-only remote-signer, standalone testing, and hardened mainnet setups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill with real funds before hardening can expose wallet or signing authority.

Mitigation: Use disposable testnet, signet, or regtest setups unless the node is hardened for production.

Risk: Admin APIs and admin macaroons can grant broad control over the node.

Mitigation: Bind admin APIs to localhost or an internal network and replace admin macaroons with least-privilege signing credentials.

Risk: Standalone mode stores wallet passphrases and seed material on disk.

Mitigation: Prefer a separate remote signer for mainnet use and avoid plaintext seed or passphrase storage.

Risk: Credential archive import can introduce sensitive or unexpected files.

Mitigation: Validate credential archives before extraction and restrict credential file permissions.

Risk: Unverified images or source releases can introduce supply-chain risk.

Mitigation: Pin or verify Docker images and source releases before deployment.

## Reference(s):

- [LND Wallet Security Guide](references/security.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local Docker, LND, wallet, signer, and credential files when the generated commands are executed.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
