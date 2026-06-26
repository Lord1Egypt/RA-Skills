## Description: <br>
Routes supported DeFi DApp and protocol-token prompts to the matching OKX plugin-store skill, installs that plugin when needed, and forwards the user's request for protocol-specific handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to resolve named DeFi protocols or protocol-native tokens to the appropriate OKX plugin, then continue with trading, betting, staking, borrowing, transfer, or other protocol-specific workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add global crypto plugins and route trading, betting, transfer, approval, or staking requests to downstream plugins. <br>
Mitigation: Review before installing, and confirm the downstream plugin, amounts, destination, wallet approval, and spending limits before executing or signing. <br>
Risk: A routing error or ambiguous DApp request could send the user's prompt to an unintended protocol plugin. <br>
Mitigation: Use the skill's confidence and clarification flow for ambiguous requests, and inspect the selected plugin's quickstart before continuing. <br>


## Reference(s): <br>
- [OKX Web3](https://web3.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install downstream OKX plugin-store skills globally before forwarding the user's original request.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
