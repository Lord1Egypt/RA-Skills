## Description: <br>
HypurrFi helps agents manage DeFi lending on Hyperliquid by checking positions and health, depositing assets for yield, borrowing against collateral, withdrawing, and repaying. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lastandy](https://clawhub.ai/user/lastandy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and DeFi treasury operators use this skill to manage HypurrFi lending workflows on Hyperliquid, including wallet setup, position review, deposits, withdrawals, borrowing, repayment, and liquidation-risk checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or uses a persistent plaintext hot-wallet private key for DeFi transactions. <br>
Mitigation: Use a dedicated low-balance wallet, restrict filesystem access to the wallet file, and avoid reusing keys that protect significant funds. <br>
Risk: The skill can authorize real deposits, withdrawals, borrows, repayments, and token approvals. <br>
Mitigation: Review previews before execution, avoid unattended --yes usage, start with small amounts, and revoke token allowances after repayment or testing. <br>
Risk: Borrowing can increase liquidation risk if collateral value falls or health factor is low. <br>
Mitigation: Check health factor before borrowing, keep conservative collateral buffers, and monitor positions regularly. <br>
Risk: Some documented markets, rate checks, and contract addresses are unsupported or incomplete in this version. <br>
Mitigation: Verify contract addresses independently and treat Prime, Yield, Vault, and rates examples as unsupported until validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lastandy/hypurrfi) <br>
- [Publisher profile](https://clawhub.ai/user/lastandy) <br>
- [HypurrFi homepage](https://hypurr.fi) <br>
- [HypurrFi app](https://app.hypurr.fi) <br>
- [HypurrFi docs](https://docs.hypurr.fi) <br>
- [Hyperliquid explorer](https://explorer.hyperliquid.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet setup details, transaction previews, transaction hashes, position summaries, health-factor reports, and error guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
