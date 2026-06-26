## Description: <br>
Lokuli Booking helps agents search, check availability, and book real-world local services through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find nearby service providers, compare service details and pricing, check availability, and create confirmed bookings with payment handled through Stripe checkout links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create real service bookings and payment checkout links. <br>
Mitigation: Confirm the provider, service, price, appointment time, and contact details with the user before creating a booking or cart. <br>
Risk: Booking workflows may share personal, contact, location, and booking details with Lokuli and payment details with Stripe. <br>
Mitigation: Proceed only after the user is comfortable sharing the required name, email, phone, ZIP or location, and booking details. <br>


## Reference(s): <br>
- [ClawHub Lokuli Booking listing](https://clawhub.ai/edwardrodriguez703-design/lokuli-skills) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-RPC request examples and service, availability, booking, or checkout results from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before booking or cart creation; booking completion may return a Stripe checkout URL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
