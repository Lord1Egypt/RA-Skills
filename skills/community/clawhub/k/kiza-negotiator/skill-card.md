## Description: <br>
Kiza Negotiator is an agent skill for automating marketplace negotiations, offer responses, deal closing, and pricing with configurable negotiation styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamskark](https://clawhub.ai/user/iamskark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators, service providers, and bounty participants use this skill to draft or automate negotiation responses, bidding behavior, pricing choices, and deal-flow actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may receive marketplace account authority and perform autonomous bidding, counter-offers, escrow steps, or deal closure without clear safety limits. <br>
Mitigation: Use a dedicated or least-privilege marketplace account, keep auto-respond and auto-pilot disabled until tested, and require manual approval for bids, counter-offers, escrow steps, and deal closure. <br>
Risk: The actual kiza-nego implementation is not included in the artifact evidence reviewed for this card. <br>
Mitigation: Verify the implementation before installation, set strict financial limits, confirm how to stop the agent, and confirm how negotiation logs can be deleted. <br>


## Reference(s): <br>
- [Kiza Negotiator on ClawHub](https://clawhub.ai/iamskark/kiza-negotiator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or initiate marketplace negotiation actions depending on the account authority and runtime configuration granted by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
