## Description: <br>
The Agent Payment Rails Playbook helps agent builders ship multi-protocol payments across x402, ACP, AP2, UCP, and MPP with spending controls, KYA compliance, and escrow protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders use this guide to design payment flows that combine agent discovery, authorization, settlement, escrow, spending controls, dispute handling, and production monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment examples can create or confirm payment, deposit, escrow, dispute, settlement, signing, or webhook actions if pointed at live endpoints with real credentials. <br>
Mitigation: Run examples only in sandbox or test mode until deliberately configured for production, and require explicit human approval for money-moving or signing actions. <br>
Risk: The guide mixes sandbox guidance with live-production endpoint language, which can lead to accidental use of production services. <br>
Mitigation: Review endpoint configuration before use, replace live-style placeholders, and keep sandbox and production credentials separated. <br>
Risk: The examples reference sensitive credentials for GreenHelix, agent signing, and Stripe. <br>
Mitigation: Use narrowly scoped keys, store credentials in a managed secret store, rotate exposed keys, and avoid pasting live secrets into prompts, logs, or sample files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mirni/greenhelix-agent-payment-rails-playbook) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>
- [x402 facilitator](https://x402.org/facilitator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference GREENHELIX_API_KEY, AGENT_SIGNING_KEY, and STRIPE_API_KEY.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
