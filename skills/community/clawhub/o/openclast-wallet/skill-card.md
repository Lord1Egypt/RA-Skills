## Description: <br>
Guides agents through Openclast/Openclaw wallet setup, balances, transactions, approvals, and key export safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide wallet setup, balance checks, transaction preparation, approvals, contract operations, and private-key export handling for Openclast/Openclaw wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outgoing transactions, token approvals, and contract operations can move assets or grant permissions if the user approves the wrong recipient, chain, amount, contract, or scope. <br>
Mitigation: Keep approval mode enabled and verify recipient, chain, amount, contract, and approval scope before broadcasting. <br>
Risk: Private-key export can expose wallet credentials and lead to asset loss. <br>
Mitigation: Avoid private-key export unless absolutely necessary; require explicit confirmation and use host-supported export gates when available. <br>
Risk: The skill depends on separate wallet CLI or host wallet tools for execution. <br>
Mitigation: Install and use only trusted wallet tooling, and treat this skill as guidance rather than a wallet implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fabriziogianni7/openclast-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration keys] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; does not broadcast transactions itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
