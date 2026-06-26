## Description: <br>
Helps an agent submit fulfillment text for an existing NLA escrow, check arbitration results, and collect approved funds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers working with NLA escrows use this skill to prepare fulfillment text, run nla CLI commands for fulfill, status, and collect operations, and understand the approval-dependent collection flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet-backed blockchain escrow transactions, including fulfill and collect operations that may spend gas, require bonds, or move escrowed tokens. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit confirmation of the network, wallet address, escrow UID, fulfillment UID, oracle address, gas and bond costs, destination or recipient, and exact fulfillment text before running transaction commands. <br>
Risk: Fulfillment text is permanently recorded on-chain and may be evaluated by an oracle before collection is possible. <br>
Mitigation: Review the demand and fulfillment text carefully, avoid private or sensitive information, and verify arbitration status before attempting collection. <br>


## Reference(s): <br>
- [Nla Fulfill release page](https://clawhub.ai/mlegls/nla-fulfill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples and fulfillment text suggestions for user review before wallet-backed execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
