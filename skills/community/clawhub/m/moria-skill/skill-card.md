## Description: <br>
A Web3 wallet management skill for Moria.fun that lets an agent create, mint, trade, refund, and claim tokens and manage wallet balances and deposits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miyeon9057](https://clawhub.ai/user/miyeon9057) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate Moria.fun token workflows, including token creation, minting, buying, selling, refunding, fee claiming, balance checks, and deposit support. Developers and reviewers should treat its wallet and transaction behavior as sensitive because it can control a configured Moria/Solana wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign mainnet wallet transactions for token creation, minting, buying, selling, refunding, and claiming. <br>
Mitigation: Use only a dedicated, low-balance wallet and require a plain-language transaction summary and user confirmation before every wallet-affecting action. <br>
Risk: Recoverable wallet key material and account data are stored locally in config/config.json. <br>
Mitigation: Treat config/config.json as sensitive credentials, never echo its raw contents, and rotate or replace credentials if exposure is suspected. <br>
Risk: Credential and upload behavior is under-disclosed for production use. <br>
Mitigation: Review upload paths and replace or rotate embedded Pinata and RPC credentials before production deployment. <br>
Risk: Ambiguous token addresses, amounts, or requested actions can lead to unintended transactions. <br>
Mitigation: Refuse ambiguous requests and confirm the mint address, amount, action type, and expected wallet impact before execution. <br>


## Reference(s): <br>
- [Moria.fun](https://moria.fun) <br>
- [Security Policy](references/security.md) <br>
- [ClawHub Release Page](https://clawhub.ai/miyeon9057/moria-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide or execute wallet-affecting Moria.fun actions through package scripts after configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
