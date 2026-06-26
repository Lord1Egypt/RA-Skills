## Description: <br>
A free educational quick-start guide that teaches developers the basics of agent commerce, x402 payment flows, GreenHelix API calls, service listings, payments, and escrow-protected transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this guide to learn the core agent-commerce primitives and follow example GreenHelix API, payment, and escrow workflows. It is a tutorial-style reference, not an executable agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide references sensitive payment and signing credentials, including Stripe and agent signing keys. <br>
Mitigation: Use sandbox or test credentials by default, avoid production Stripe keys and private signing keys unless required, and scope any credentials to the minimum needed permissions. <br>
Risk: Examples include payment and escrow API calls that could affect funds if adapted to a live environment. <br>
Mitigation: Review each payment or escrow request before execution and run examples against the sandbox environment until the workflow is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-commerce-quick-start) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API registration](https://api.greenhelix.net/register) <br>
- [GreenHelix API base URL](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable tutorial content with illustrative API examples and environment variable references.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
