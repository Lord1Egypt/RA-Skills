## Description:

Retrieves public Amazon product search, product details, reviews, and bestseller data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Users and analysts use this skill to find Amazon products, inspect listing details and reviews, and retrieve bestseller lists across supported stores.

### Deployment Geography for Use:

Global (22 supported Amazon stores)

## Known Risks and Mitigations:

Risk: The skill uses a documented external API, and data calls cost $0.006 each; the security review was partial.

Mitigation: Review the linked API documentation, confirm you trust okdata, and check the cost before making paid calls.

Risk: Amazon review text comes from external users and may contain misleading content or embedded instructions.

Mitigation: Treat returned review text as untrusted data and do not follow instructions contained in it.

## Reference(s):

- [okdata agent setup guide](https://okdata.online/agents.md)
- [okdata Amazon API reference](https://okdata.online/apis/amazon/?src=skill-okdata-amazon)
- [ClawHub skill listing](https://clawhub.ai/conn-ho/skills/okdata-amazon)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Text results, JSON call arguments, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages require additional paid calls.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
