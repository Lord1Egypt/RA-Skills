## Description: <br>
Delegate Aavegotchi petting rights to AAI's wallet on Base, generate approve and revoke transaction data, check approval, and maintain delegated wallet bookkeeping in pet-me-master config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Aavegotchi users and operators use this skill to prepare pet-operator approval or revocation transactions on Base and keep local delegation bookkeeping aligned after on-chain approval changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may sign approval data for the wrong contract, operator address, network, or calldata. <br>
Mitigation: Verify the Aavegotchi Diamond contract, AAI operator address, Base network, and decoded calldata in a wallet or trusted explorer before signing. <br>
Risk: Bookkeeping scripts persistently edit the local pet-me-master configuration and create backup files. <br>
Mitigation: Review PET_ME_CONFIG_FILE before running add or remove scripts, and inspect the generated backup if a local configuration change needs to be restored. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaigotchi/pet-operator) <br>
- [README](artifact/README.md) <br>
- [Revocation Guide](artifact/REVOKE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and transaction details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cast and jq; generated transaction data is intended for user review before signing.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
