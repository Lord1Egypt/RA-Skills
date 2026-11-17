## Description:

Book real-world services through Lokuli MCP. Use when user needs to find, check availability, or book local services like plumbers, electricians, cleaners, mechanics, barbers, personal trainers, etc. Triggers on requests like "book me a haircut", "find a plumber near me", "I need a smog check", "schedule a massage", or any local service request. 75+ service categories available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for local service providers, compare pricing and availability, and create bookings through Lokuli after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to Lokuli's external MCP service and may share ZIP code, service request, selected time, name, email, and phone details.

Mitigation: Use it only when the user intends to search or book a local service, and collect only the details required for the booking.

Risk: The skill can create a real-world booking and payment checkout flow.

Mitigation: Confirm provider, service, pricing, time, and customer details with the user before creating any booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with JSON-RPC tool-call examples and external checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a Stripe checkout URL after user confirmation and required customer details are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
