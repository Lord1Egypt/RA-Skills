## Description: <br>
Safely operate the nova CLI wallet for authentication, balance checks, sending funds, withdrawals, and key management across mainnet and testnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SynthLuvr](https://clawhub.ai/user/SynthLuvr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent assist with nova CLI wallet workflows, including login, balance checks, transfers, withdrawals, claim links, and key management while preserving explicit human confirmation for financial actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet operations can move real funds or create claim links. <br>
Mitigation: Before any send or withdrawal, personally verify the network, amount, recipient, blockchain, and stablecoin; use dry-run previews where supported and never retry non-idempotent sends blindly. <br>
Risk: Wallet secrets, login codes, recovery phrases, private keys, and claim links can expose funds if shared or logged. <br>
Mitigation: Keep secrets out of shared chats, tickets, logs, and long-term agent memory, and warn users before any export operation. <br>
Risk: The skill relies on the upstream nova CLI package for wallet behavior. <br>
Mitigation: Install and use this skill only when you trust the upstream nova CLI package and intend to let an agent assist with wallet operations. <br>


## Reference(s): <br>
- [Nova CLI Reference](artifact/references/REFERENCE.md) <br>
- [Nova GitHub Project](https://github.com/MynthAI/nova) <br>
- [Nova npm Package](https://www.npmjs.com/package/@mynthai/nova) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured JSON or TOON parsing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent outputs should confirm exit codes and structured status fields before treating nova CLI results as successful.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
