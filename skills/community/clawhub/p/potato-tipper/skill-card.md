## Description: <br>
Skill for AI agents to setup the Potato Tipper on a Universal Profile on LUKSO (requires private key), and learn to build innovative tip-on-follow solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CJ42](https://clawhub.ai/user/CJ42) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to understand, configure, and troubleshoot Potato Tipper integrations for LUKSO Universal Profiles, including permissions, data keys, and tip-on-follow workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow uses a raw private key and can broadcast transactions. <br>
Mitigation: Use a dedicated low-balance controller, avoid production private keys in commands or shared terminals, and simulate where possible before broadcasting. <br>
Risk: The setup can grant token-spending permission and Universal Profile delegate settings. <br>
Mitigation: Verify cloned code and contract addresses, choose the smallest tipping budget, and confirm how to revoke the $POTATO operator approval and delegate settings. <br>
Risk: Incorrect Universal Profile permissions can cause failed setup or leave broader access than needed. <br>
Mitigation: Grant only the required controller permissions for the task and remove or narrow them after setup when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CJ42/potato-tipper) <br>
- [README](README.md) <br>
- [Potato Tipper contracts](https://github.com/CJ42/potato-tipper-contracts) <br>
- [Deployed contract addresses](references/addresses.md) <br>
- [Config and data keys](references/config-and-data-keys.md) <br>
- [Permissions](references/permissions.md) <br>
- [Foundry batch setup](references/foundry-batch-setup.md) <br>
- [Security and limitations](references/security-and-limitations.md) <br>
- [TypeScript examples](references/typescript-examples.md) <br>
- [Solidity examples](references/solidity-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, TypeScript, and Solidity examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include transaction setup guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
