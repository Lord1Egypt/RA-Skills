## Description: <br>
Manage trust-based agent credit lines, track balances and transactions, and settle payments via the X402 stablecoin protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levi-law](https://clawhub.ai/user/levi-law) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use MoltCredit to register agents, extend trust-based credit lines, record bilateral transactions, inspect balances and history, and generate X402 settlement requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands can change credit lines, transaction records, and settlement state through the MoltCredit API. <br>
Mitigation: Keep the API key out of logs and prompts, use a limited account if possible, and require manual review before extend-credit, transact, or settle commands. <br>
Risk: Server security evidence says the skill gives an agent authority to change financial credit, transaction, and settlement records without strong confirmation or guardrails. <br>
Mitigation: Require explicit approval of counterparties, credit limits, transaction amounts, currencies, and settlement requests before running mutating commands. <br>


## Reference(s): <br>
- [MoltCredit ClawHub page](https://clawhub.ai/levi-law/moltcredit) <br>
- [MoltCredit API docs](https://moltcredit-737941094496.europe-west1.run.app/skill.md) <br>
- [MoltCredit landing page](https://levi-law.github.io/moltcredit-landing) <br>
- [X402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated requests use MOLTCREDIT_API_KEY; mutating credit, transaction, and settlement commands should be manually reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
