## Description:

Book real-world services through Lokuli MCP by helping an agent find providers, check availability, estimate pricing, and create confirmed local-service bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search local service providers, compare pricing and availability, and create bookings only after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A booking or payment link could be created for the wrong provider, price, time, or contact details.

Mitigation: Confirm provider, price, time, and customer contact details with the user before creating any booking or payment link.

Risk: The skill could be invoked for generic service advice when the user does not intend to search for or schedule a real service.

Mitigation: Use the skill only for local service searches and bookings, and answer generic advice requests without initiating Lokuli booking actions.

Risk: A requested ZIP code or location may not be serviceable.

Mitigation: Validate the location before presenting booking options or attempting to create a booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/lokuli-skills)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown/text with JSON-RPC tool call examples and checkout URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before booking; payment is completed through a Stripe checkout URL.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
