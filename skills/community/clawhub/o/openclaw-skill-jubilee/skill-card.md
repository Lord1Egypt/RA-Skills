## Description: <br>
Helps OpenClaw agents manage treasury funds across Base, Solana, and Ethereum using Jubilee Protocol vaults for yield, balances, deposits, withdrawals, donations, and strategic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prayingperceptions](https://clawhub.ai/user/prayingperceptions) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to inspect vault status, review treasury balances, deposit or withdraw assets, donate yield, and generate treasury strategy reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that move real crypto funds using a raw wallet key. <br>
Mitigation: Use a new low-balance wallet, avoid main wallets, verify every transaction manually, and confirm each contract and recipient before execution. <br>
Risk: Automated yield donation jobs may send funds without sufficient operator review. <br>
Mitigation: Avoid automated donation schedules until the implementation and transaction safeguards have been reviewed. <br>
Risk: The war-room workflow inspects repository activity and may run in workspaces that contain secrets. <br>
Mitigation: Run war-room only in repositories that do not contain secrets or sensitive wallet material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prayingperceptions/openclaw-skill-jubilee) <br>
- [Jubilee Protocol documentation](https://docs.jubileeprotocol.xyz) <br>
- [Jubilee Protocol GitHub](https://github.com/Jubilee-Protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transaction-oriented command guidance and treasury reports that require manual review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
