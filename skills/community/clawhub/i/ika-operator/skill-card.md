## Description: <br>
Guide for operating Ika network nodes, including validators, fullnodes, and notifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omersadika](https://clawhub.ai/user/omersadika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and Ika infrastructure operators use this skill to deploy, configure, monitor, and troubleshoot Ika validators, fullnodes, and notifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validator keys, especially the root seed, can be lost or exposed during setup or operations. <br>
Mitigation: Back up validator keys immediately, keep root seed backups offline, and treat key material with the same caution as funds. <br>
Risk: Incorrect binaries, contract IDs, staking URLs, or chain configuration can lead to failed or unsafe node operation. <br>
Mitigation: Verify binaries, package and object IDs, staking links, and configuration values against official Ika sources before executing commands. <br>
Risk: Database recovery commands can delete local node state. <br>
Mitigation: Use deletion-based recovery only as a last resort after confirming the exact path and backup or resync plan. <br>
Risk: Example object-store or metrics proxy configuration can be misused to store real secrets in files or repositories. <br>
Mitigation: Do not commit real AWS credentials or other secrets; use secret management appropriate for the deployment environment. <br>


## Reference(s): <br>
- [Complete Configuration Reference](references/configuration.md) <br>
- [Operations Reference](references/operations.md) <br>
- [Mainnet Validator Setup](references/validator-setup.md) <br>
- [Ika homepage](https://ika.xyz) <br>
- [Ika releases](https://github.com/dwallet-labs/ika/releases) <br>
- [Mainnet deployed contract addresses](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/mainnet/address.yaml) <br>
- [Testnet deployed contract addresses](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/testnet/address.yaml) <br>
- [Ika Operator ClawHub release](https://clawhub.ai/omersadika/ika-operator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only operational guidance; commands and configuration values require operator review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
