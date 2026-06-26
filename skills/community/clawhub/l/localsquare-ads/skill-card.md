## Description: <br>
Helps agents find LocalSquare board availability and reserve paid public advertising pins for local businesses after user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThatDudeFreak](https://clawhub.ai/user/ThatDudeFreak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and business-support agents use this skill to discover available LocalSquare advertising space for a ZIP-code market and reserve a public business pin. It is intended for local advertising workflows where the user explicitly approves payment, placement, and public listing details. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: A wallet payment could be approved for the wrong domain, facilitator, recipient, network, amount, town, or square position. <br>
Mitigation: Before any wallet approval, verify the domain, x402 facilitator, recipient, Base network, amount, town, and square position with the user. <br>
Risk: Raw private keys or signing secrets could be exposed if entered into an agent prompt or configuration. <br>
Mitigation: Use only secure external wallet signing such as a hardware wallet, browser extension, or WalletConnect, and never provide raw private keys to the agent. <br>
Risk: Business details submitted through the skill are intended to become public and searchable. <br>
Mitigation: Review the business name, contact details, address, image, and description with the user before submitting a claim. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ThatDudeFreak/localsquare-ads) <br>
- [LocalSquare Homepage](https://yourlocalsquare.com) <br>
- [LocalSquare AI Documentation](https://yourlocalsquare.com/llms.txt) <br>
- [Agent API Status](https://yourlocalsquare.com/api/agent/status) <br>
- [x402 Discovery](https://yourlocalsquare.com/.well-known/x402.json) <br>
- [x402 Protocol](https://x402.org) <br>
- [Privacy Policy](https://yourlocalsquare.com/privacy) <br>
- [Terms of Service](https://yourlocalsquare.com/terms) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with HTTP examples, JSON request and response bodies, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing workflow guidance for discovery, user confirmation, x402 payment handling, and public listing follow-up.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
