## Description: <br>
Shadow HR Infrastructure. Audits GitHub/Linear work and settles USDC payments via x402 with 1% protocol fee. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eldan445](https://clawhub.ai/user/Eldan445) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External teams, developers, and agents use this skill to audit GitHub pull requests or Linear work items before calculating contractor payouts and a 1% USDC protocol fee. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles USDC payroll settlement, and the security evidence reports that audit checks always pass, which could approve payments for unverified work. <br>
Mitigation: Do not use for real payroll unless audit checks fail closed and every payment requires explicit confirmation of recipient, amount, network, fees, and reviewed evidence before settlement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Eldan445/payroll-oracle) <br>
- [Publisher profile](https://clawhub.ai/user/Eldan445) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Plain text and Markdown-style agent guidance with Python script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calculates worker payout and protocol fee from a single amount; audit scripts should require explicit verification before settlement.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
