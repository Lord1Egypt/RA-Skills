## Description:

Book real-world services through Lokuli MCP. Use when user needs to find, check availability, or book local services like plumbers, electricians, cleaners, mechanics, barbers, personal trainers, etc. Triggers on requests like "book me a haircut", "find a plumber near me", "I need a smog check", "schedule a massage", or any local service request. 75+ service categories available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and assistants use this skill to search for local service providers, compare pricing and availability, and create confirmed bookings through Lokuli with Stripe checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can share booking contact details with Lokuli's external MCP service.

Mitigation: Collect only the required name, email, and phone information after the user selects a provider, service, and time.

Risk: The skill can generate payment checkout links for real-world services.

Mitigation: Review the provider, service, time, and price with the user and require explicit approval before creating a booking or sharing the checkout link.

Risk: Service availability, location coverage, and pricing may vary by provider and ZIP code.

Mitigation: Validate the location, check current availability, and present pricing information before confirmation.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/lokuli-booking)
- [ClawHub publisher profile](https://clawhub.ai/user/edwardrodriguez703-design)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown prose with JSON-RPC MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Stripe checkout links through Lokuli MCP after explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
