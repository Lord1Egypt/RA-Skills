## Description: <br>
Create x402 USDC payment links using the OpenPayment CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vittominacori](https://clawhub.ai/user/vittominacori) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, merchants, creators, and AI agents use this skill to create OpenPayment-hosted x402 USDC payment links, including single-use, reusable, variable-amount, and proxy links on Base networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Base Mainnet links involve real USDC payment requests. <br>
Mitigation: Confirm the amount, recipient wallet address, network, and description with the user before creating a link. <br>
Risk: Proxy payment links can include an upstream resource URL and financial details. <br>
Mitigation: Confirm the proxy URL before creation and avoid requesting or sharing private keys or secrets. <br>


## Reference(s): <br>
- [OpenPayment homepage](https://openpayment.link) <br>
- [OpenPayment ClawHub release](https://clawhub.ai/vittominacori/openpayment) <br>
- [OpenPayment publisher profile](https://clawhub.ai/user/vittominacori) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; the CLI returns plain text or JSON payment-link output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create OpenPayment-hosted USDC payment links after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
