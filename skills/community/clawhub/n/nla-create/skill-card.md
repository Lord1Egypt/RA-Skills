## Description: <br>
Create a Natural Language Agreement escrow on-chain for locking ERC20 tokens with a natural language demand that an AI oracle will arbitrate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create ERC20-backed Natural Language Agreement escrows, gather required transaction parameters, craft an evaluable demand, and run the nla CLI to create the escrow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help lock ERC20 tokens in an on-chain escrow, so incorrect network, token, amount, oracle, or demand choices can cause financial loss or unusable escrows. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit confirmation of the network, token, amount, oracle, and demand before running escrow creation. <br>
Risk: Wallet private keys may be exposed if entered into chat or passed directly on the command line. <br>
Mitigation: Avoid pasting private keys into chat or commands; prefer secure wallet configuration outside the agent session. <br>
Risk: Demand text and arbitration settings may become public on-chain. <br>
Mitigation: Keep secrets and private data out of demands, prompts, and arbitration settings, and warn users before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mlegls/nla-create) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes escrow UID reporting and next-step guidance after command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
