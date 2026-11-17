## Description:

Pipe17 Openclaw Skill helps agents search and read Pipe17 orders, shipping requests, fulfillments, and inventory through the Pipe17 Unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-shao1](https://clawhub.ai/user/j-shao1)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to let an agent retrieve Pipe17 commerce and fulfillment data for support, inventory, and order-status workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped Pipe17 API key could expose more business data than the workflow requires.

Mitigation: Use a read-only or least-privilege Pipe17 key for the target organization or integration.

Risk: Returned order, shipment, fulfillment, and inventory data may contain sensitive business information.

Mitigation: Treat API responses as sensitive and limit sharing, logging, and retention to the business need.

Risk: Broad unfiltered searches can retrieve unnecessary operational data.

Mitigation: Use narrow status, date, SKU, location, or identifier filters whenever practical.

## Reference(s):

- [Pipe17 Unified API Docs](https://apidoc.pipe17.com/#/)
- [ClawHub Skill Page](https://clawhub.ai/j-shao1/skills/pipe17-openclaw-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Pipe17 API key and favors read-only, filtered API requests.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
