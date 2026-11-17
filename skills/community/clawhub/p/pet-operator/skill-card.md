## Description:

Delegate Aavegotchi petting rights to AAI's wallet on Base, generate approve and revoke transaction data, check approval, and maintain delegated wallet bookkeeping in pet-me-master config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT

## Use Case:

Aavegotchi users and operators use this skill to prepare pet-operator approval or revocation transactions on Base and keep local delegated-wallet records aligned after approval state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated approve or revoke calldata may use the default AAI operator if operator overrides are not reflected as expected.

Mitigation: Decode or independently verify every generated transaction before signing, especially when overriding AAI_OPERATOR.

Risk: Delegated-wallet scripts modify local pet-me-master configuration and create backup files.

Mitigation: Confirm PET_ME_CONFIG_FILE points to the intended config and review the resulting configuration changes after add or remove operations.

Risk: On-chain approval grants pet-operator rights for all gotchis owned by the wallet.

Mitigation: Use the generated revoke transaction when delegation is no longer intended and confirm the transaction target, calldata, and Base network before signing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaigotchi/skills/pet-operator)
- [Base Mainnet RPC](https://mainnet.base.org)
- [MyEtherWallet Access](https://www.myetherwallet.com/wallet/access)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with transaction calldata, approval status, and configuration update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cast and jq for chain reads and JSON configuration updates.]

## Skill Version(s):

1.2.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
