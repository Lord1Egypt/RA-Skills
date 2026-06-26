## Description: <br>
Operate the Payall crypto card CLI tool for card browsing, card management, USDT-funded top-ups and withdrawals, wallet balances, and on-chain USDT transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c0ldsmi1e](https://clawhub.ai/user/c0ldsmi1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the Payall CLI for crypto debit card discovery, card account operations, USDT top-ups and withdrawals, wallet balance checks, and USDT transfers across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through wallet authentication and operations that involve private keys. <br>
Mitigation: Use a dedicated low-balance wallet, avoid using a main wallet private key, and review the skill before installation. <br>
Risk: The skill can expose full card numbers, CVV values, and billing details when reveal commands are used. <br>
Mitigation: Reveal full card or CVV data only when necessary for a user-approved task and avoid storing or sharing the revealed data. <br>
Risk: The skill documents confirmation-skipping flags for transfers, card applications, top-ups, and withdrawals. <br>
Mitigation: Require explicit human confirmation for every amount, chain, destination, card application, top-up, withdrawal, or transfer before running commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/c0ldsmi1e/payall-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/c0ldsmi1e) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command sequences for Payall CLI authentication, card operations, wallet checks, top-ups, withdrawals, and transfers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
