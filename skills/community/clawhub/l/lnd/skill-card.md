## Description: <br>
Installs and operates Lightning Terminal (litd) for lnd-based payments, channel management, liquidity tools, Taproot Assets, and L402 commerce with Docker, native, watch-only, standalone, and regtest modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operators use this skill to install, configure, start, stop, and query a Lightning Terminal or lnd node for payments, channel operations, liquidity management, Taproot Assets, and agent L402 commerce. It is suited to testnet-first setup, watch-only remote-signer operation, standalone testing, and local regtest development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes high-impact wallet and signing workflows for a Lightning node. <br>
Mitigation: Install only if you understand Lightning node operations, keep the default on testnet until verified, and avoid mainnet funds unless network ports are firewalled or bound to localhost. <br>
Risk: Standalone mode can place wallet passphrases and seed material on disk. <br>
Mitigation: Prefer the watch-only remote-signer model, keep standalone mode to testing or small-risk use, and ensure wallet and recovery backups are secured before handling funds. <br>
Risk: Admin macaroons and signer credential bundles can grant broad Lightning-node authority. <br>
Mitigation: Use least-privilege macaroons, import credential bundles only from a trusted signer, and replace admin macaroons with scoped credentials for production use. <br>
Risk: Cleanup with volume removal can destroy node data needed for wallet or channel recovery. <br>
Mitigation: Do not run cleanup with volume removal unless wallet seed, channel state, and recovery procedures are fully backed up and verified. <br>


## Reference(s): <br>
- [LND Wallet Security Guide](references/security.md) <br>
- [ClawHub Lnd skill page](https://clawhub.ai/Roasbeef/lnd) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run Docker, wallet, credential-import, and Lightning CLI workflows through bundled shell scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
