## Description: <br>
Book real-world local services through Lokuli MCP by helping users search providers, check availability, and create bookings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and assistants use this skill to find local service providers, compare pricing and availability, and prepare bookings through Lokuli. The workflow requires explicit user confirmation before creating a booking or sharing a payment link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A booking may be created for the wrong provider, service, time, price, or cancellation terms. <br>
Mitigation: Verify the provider, service, time, price, cancellation terms, and contact details with the user before approving any booking. <br>
Risk: The workflow may share ZIP code, contact information, or payment-flow details with Lokuli, the provider, or Stripe-linked checkout. <br>
Mitigation: Collect only the information needed for the booking and make the external sharing and payment-link step clear before proceeding. <br>


## Reference(s): <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/lokuli-booking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries with JSON-RPC tool-call arguments and booking or payment links when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider details, availability windows, estimated pricing, customer-contact prompts, and Stripe checkout URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
