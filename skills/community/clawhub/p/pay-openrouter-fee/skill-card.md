## Description: <br>
Top up or pay OpenRouter (or similar LLM billing) from your CAI custodial wallet after the agent finds the payee details and you confirm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent prepare OpenRouter or similar LLM billing payments from a CAI custodial wallet after the user confirms the payee, amount, chain, and token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare real wallet payments, and transfers may not be recoverable if sent to the wrong recipient. <br>
Mitigation: Before any transfer, independently verify the OpenRouter billing recipient, amount, chain, token, and account crediting path, then require explicit user confirmation. <br>
Risk: The skill requires a sensitive CAI API key. <br>
Mitigation: Store the key with the agent secrets mechanism and do not paste private credentials into chat or generated instructions. <br>
Risk: Billing details discovered by the agent may be incomplete, stale, or spoofed. <br>
Mitigation: Confirm payment instructions against the active OpenRouter billing page or official billing source before resolving a recipient or address. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/bernardtai/pay-openrouter-fee) <br>
- [CAI skill reference](https://cai.com/skill.md) <br>
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md) <br>
- [CAI agent payment](https://cai.com/agent-payment.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and ordered task steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY and explicit user confirmation before transfer.] <br>

## Skill Version(s): <br>
1.0.15 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
