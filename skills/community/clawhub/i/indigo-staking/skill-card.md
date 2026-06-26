## Description: <br>
Query and manage INDY token staking positions on Indigo Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Indigo Protocol staking state and prepare INDY staking, adjustment, closing, and reward-distribution actions for wallet review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare crypto staking transactions that may move or lock assets if signed. <br>
Mitigation: Verify the wallet address, staking position, amount units, fees, rewards, and resulting asset movement before signing any returned CBOR transaction. <br>
Risk: Returned CBOR values depend on the Indigo MCP provider and may not include enough confirmation guidance by themselves. <br>
Mitigation: Install and use the skill only with a trusted Indigo MCP provider, and treat each CBOR value as a transaction proposal requiring independent wallet review. <br>


## Reference(s): <br>
- [Indigo Staking ClawHub Release](https://clawhub.ai/adacapo21/indigo-staking) <br>
- [Staking MCP Tools Reference](artifact/references/mcp-tools.md) <br>
- [Staking Concepts](artifact/references/concepts.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, API calls, configuration] <br>
**Output Format:** [Markdown guidance with MCP tool names, parameters, JSON examples, and unsigned transaction CBOR outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations can return unsigned Cardano transaction CBOR that must be inspected and signed outside the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
