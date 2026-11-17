## Description:

Book real-world services through Lokuli MCP for finding, checking availability, and booking local services across 75+ service categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search local service providers, compare pricing and availability, and create user-confirmed bookings through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking flows can share customer contact and location details with Lokuli.

Mitigation: Confirm provider, time, price, and the information being sent before approving any booking or payment link.

Risk: A booking or payment link could be created before the user has fully reviewed the selected service.

Mitigation: Require explicit user approval before creating a booking and show pricing upfront.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub Local Booking skill page](https://clawhub.ai/edwardrodriguez703-design/skills/local-booking)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Markdown with structured MCP tool call arguments and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return provider search results, availability, pricing estimates, booking status, and Stripe checkout URLs after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
