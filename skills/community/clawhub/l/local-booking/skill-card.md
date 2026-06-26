## Description: <br>
Book real-world services through Lokuli MCP by finding local providers, checking availability, and creating bookings for services such as plumbers, electricians, cleaners, mechanics, barbers, and personal trainers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for local-service providers, compare pricing and availability, and create a booking through Lokuli after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking creation may share contact details and service request information with Lokuli and payment providers. <br>
Mitigation: Review the provider, service, time, price, and contact details with the user before creating a booking or opening a checkout link. <br>
Risk: A booking or payment link could be created before the user has confirmed the provider, availability, or price. <br>
Mitigation: Require explicit user approval, show pricing upfront, and collect required contact information before calling the booking workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/local-booking) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown with JSON-RPC examples and booking workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP tool requests for search, provider detail lookup, availability checks, booking creation, booking status, catalog lookup, pricing estimates, location validation, and cart creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
