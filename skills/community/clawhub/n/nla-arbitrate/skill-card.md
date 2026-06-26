## Description: <br>
Manually arbitrate NLA escrow fulfillments as an alternative to the automated oracle, with support for interactive review and LLM-assisted auto arbitration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they are the oracle for NLA escrows and need an agent to help review pending fulfillment requests, compare demands with fulfillments, and submit arbitration decisions through the nla CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help submit permanent blockchain arbitration decisions, including bulk automatic decisions, using a funded wallet. <br>
Mitigation: Prefer interactive mode, verify each escrow and fulfillment before deciding, use a dedicated low-balance oracle wallet, and avoid bulk auto arbitration unless the operator accepts model error risk, gas costs, and irreversible on-chain outcomes. <br>
Risk: Auto mode can rely on LLM API keys and model judgments for arbitration decisions. <br>
Mitigation: Use auto mode only with approved provider credentials, review the selected provider and model for each escrow, and keep API keys scoped and managed outside the skill text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mlegls/nla-arbitrate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide commands that submit permanent on-chain arbitration attestations and can use LLM API keys in auto mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
