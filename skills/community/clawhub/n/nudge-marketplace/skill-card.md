## Description: <br>
Guides agents through browsing, submitting, and managing Nudge marketplace agent listings with documented API and x402 payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xrichyrich](https://clawhub.ai/user/0xrichyrich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to discover marketplace agents and prepare agent submissions for the Nudge platform. It provides API examples, payment-flow guidance, and marketplace listing details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment instructions conflict across the artifact and could cause payment to the wrong network, token, amount, or recipient. <br>
Mitigation: Before submitting an agent or paying a listing fee, independently verify the official domain, token, network, amount, recipient wallet, and current x402 response. <br>
Risk: Example code normalizes raw private-key token transfers. <br>
Mitigation: Do not paste a valuable wallet private key into an agent session; use a dedicated low-balance wallet or external signer and manually review any transaction. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/0xrichyrich/nudge-marketplace) <br>
- [Nudge website](https://www.littlenudge.app) <br>
- [Add Agent UI](https://www.littlenudge.app/add-agent) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON, curl, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment-flow details that should be independently verified before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
