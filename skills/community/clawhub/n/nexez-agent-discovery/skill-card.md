## Description: <br>
Discover Nexez agent pages, compare AI-ready offers, and safely hand off booking, checkout, or negotiation intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexez](https://clawhub.ai/user/nexez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover and compare Nexez marketplace listings, shortlist business offers, and prepare booking, checkout, or negotiation handoffs with explicit approval before side effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkout, negotiation, contact sharing, payment, or booking handoffs can affect real businesses or purchases. <br>
Mitigation: Use dry-run validation when possible and require explicit user approval before any real handoff or seller-facing action. <br>
Risk: Marketplace listings may omit or change seller details, prices, availability, credentials, or refund terms. <br>
Mitigation: Verify the seller, offer, price, contact details, and exact action before approving checkout, negotiation, payment, or contact sharing. <br>


## Reference(s): <br>
- [Nexez Homepage](https://nexez.ai) <br>
- [Nexez Endpoint Contract](references/endpoint-contract.md) <br>
- [Nexez Discovery Rubric](references/discovery-rubric.md) <br>
- [Nexez Skill Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API calls, Configuration] <br>
**Output Format:** [Markdown recommendations with structured shortlist details and approval prompts; API request guidance when native tools are unavailable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NEXEZ_BASE_URL as an optional base URL override. Real checkout, negotiation, contact sharing, payment, or booking actions require explicit user approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
