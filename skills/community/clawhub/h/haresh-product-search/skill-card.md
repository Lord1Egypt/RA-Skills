## Description:

Search e-commerce products via n8n webhook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haresh-sai06](https://clawhub.ai/user/haresh-sai06)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn natural language product requests into e-commerce catalog searches with category, price, and sort preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to an undocumented or placeholder webhook destination.

Mitigation: Use the skill only after replacing the endpoint with an explicit webhook that the operator controls and has reviewed.

Risk: Product search requests and webhook responses may expose unnecessary data or be handled without clear validation.

Mitigation: Minimize submitted query data, validate webhook responses, add timeout handling, and disclose the external request path to users before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haresh-sai06/skills/haresh-product-search)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON from a product-search webhook, typically summarized by the agent as user-facing text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured product-search webhook endpoint before use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
