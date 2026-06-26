## Description: <br>
Book real-world services through Lokuli MCP for finding, checking availability, and booking local services such as plumbers, electricians, cleaners, mechanics, barbers, and personal trainers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search local service providers, review pricing and availability, and create bookings through Lokuli after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global, subject to Lokuli serviceable ZIP code availability. <br>

## Known Risks and Mitigations: <br>
Risk: Booking local services can share user contact details with Lokuli and direct the user to a Stripe payment link. <br>
Mitigation: Before approving a booking or cart, verify the provider, service, time, price, cancellation terms, contact details being shared, and Stripe checkout destination. <br>
Risk: A booking or cart could be created before the user has reviewed the selected service details. <br>
Mitigation: Require explicit user confirmation before creating a booking or cart, and show pricing upfront. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/lokuli-service-booking) <br>
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with JSON-RPC tool call examples and service booking details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return provider details, availability, pricing estimates, booking status, Stripe checkout URLs, or AP2 cart data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
