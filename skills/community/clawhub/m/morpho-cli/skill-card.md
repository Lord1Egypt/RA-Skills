## Description: <br>
Interact with the Morpho lending protocol using the CLI to query vaults, markets, positions, balances, and protocol stats, and to prepare or simulate unsigned Morpho transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinmel](https://clawhub.ai/user/jinmel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and crypto operators use this skill to query Morpho lending data on Base and Ethereum and prepare unsigned transaction payloads for deposits, withdrawals, supply, borrow, collateral, and repayment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial workflows and wallet addresses through an external Morpho npm CLI. <br>
Mitigation: Install only if comfortable with that CLI, treat outputs as sensitive financial data, and avoid sharing wallet information beyond the intended command use. <br>
Risk: Incorrect chain IDs, contract addresses, amounts, approvals, borrow terms, or simulation results could lead to unwanted on-chain effects if signed later. <br>
Mitigation: Verify all transaction details and simulation results before signing anything in a wallet. <br>
Risk: Prepared transaction payloads may be misunderstood as ready to execute. <br>
Mitigation: Use the skill's unsigned-transaction posture: present summaries, warnings, and simulations, but do not sign or broadcast transactions. <br>


## Reference(s): <br>
- [Read Command Response Schemas](references/read.md) <br>
- [Write Command Response Schemas](references/write.md) <br>
- [ClawHub release page](https://clawhub.ai/jinmel/morpho-cli) <br>
- [Publisher profile](https://clawhub.ai/user/jinmel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to return JSON and prepare unsigned transactions only; the skill instructs agents not to sign or broadcast transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
