## Description: <br>
Discover and call paid third-party API services through the Nightmarket marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sistillisteph](https://clawhub.ai/user/sistillisteph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to search Nightmarket for third-party API services, inspect endpoint details, and make paid or free API calls with payment handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill can lead an agent toward remote skill installation, wallet creation, paid API calls, and persistent API-key storage without clear user consent. <br>
Mitigation: Require explicit approval before wallet setup, remote installation, payment actions, or API-key storage; keep CrowPay keys in a real secret manager. <br>
Risk: Payment and seller API calls can expose Authorization headers, private data, or spending authority to third-party services. <br>
Mitigation: Approve each payment-related action, review endpoint details before calls, and avoid sending sensitive headers or private data unless the seller is trusted. <br>


## Reference(s): <br>
- [Nightmarket API Reference](references/api.md) <br>
- [Nightmarket and CrowPay Integration](references/crow-payments.md) <br>
- [ClawHub skill page](https://clawhub.ai/sistillisteph/night-market) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service search results, endpoint details, setup guidance, and payment-flow instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
