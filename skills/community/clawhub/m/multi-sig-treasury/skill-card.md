## Description: <br>
Helps agents draft Gnosis Safe and multisig treasury setup, monitoring, governance, proposal, signer-management, and reporting guidance for DAOs and crypto treasuries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DAO operators, protocol teams, and treasury contributors use this skill to plan Safe setup, monitor balances and runway, draft spend proposals, manage signer rotation, and prepare governance documentation. It is a checklist and drafting aid; humans must approve all on-chain treasury actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Treasury guidance could be mistaken for authority to move funds. <br>
Mitigation: Use the skill only as a checklist and drafting aid; require human approval before any treasury action. <br>
Risk: Addresses, amounts, chains, signer identities, or threshold changes may be incorrect or unsafe if copied without verification. <br>
Mitigation: Manually verify Safe addresses, recipient addresses, amounts, chains, signer identities, and threshold changes in official Safe tooling, and never share seed phrases or private keys. <br>


## Reference(s): <br>
- [Multi-Sig Treasury on ClawHub](https://clawhub.ai/samledger67-dotcom/multi-sig-treasury) <br>
- [Safe Transaction Service safe info endpoint](https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/) <br>
- [Safe Transaction Service balances endpoint](https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/balances/usd/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown with checklists, tables, proposal templates, YAML snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute transactions; outputs operational drafts and verification checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
