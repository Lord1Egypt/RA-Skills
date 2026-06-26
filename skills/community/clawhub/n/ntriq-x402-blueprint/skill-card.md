## Description: <br>
AI architectural blueprint analysis that extracts rooms, dimensions, materials, and structural elements from floor plans for $0.05 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit blueprint or floor plan images to a paid remote analysis service and receive structured room, dimension, area, material, and structural-element data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blueprint images or URLs are sent to x402.ntriq.co.kr. <br>
Mitigation: Avoid confidential building plans unless the user has authorization and accepts the provider's privacy and retention practices. <br>
Risk: Each request may cost $0.05 USDC through the x402 payment flow. <br>
Mitigation: Confirm the payment header, Base mainnet network, and expected cost before issuing requests. <br>
Risk: Extracted dimensions, materials, or structural details may be incorrect or incomplete. <br>
Mitigation: Review returned analysis before using it for construction, safety, compliance, or purchasing decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/ntriq-x402-blueprint) <br>
- [ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>
- [Blueprint analysis API endpoint](https://x402.ntriq.co.kr/blueprint) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown instructions with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a paid remote service that returns structured blueprint analysis JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
