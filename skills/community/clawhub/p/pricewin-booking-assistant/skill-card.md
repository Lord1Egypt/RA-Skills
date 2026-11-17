## Description:

Recommend hotel rooms and complete real bookings end to end: reserve OpenTravel direct properties with payment links, check payment status, resend expired links, cancel bookings, and provide OTA links for comparison-only hotels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cotghw](https://clawhub.ai/user/cotghw)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and booking agents use this skill to search, compare, recommend, and book hotel rooms through approved PriceWin MCP tools, then manage payment links, booking status, and cancellations. It handles real reservations and guest contact details, so booking details and total price should be confirmed with the user before creating a reservation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real hotel reservations with payment links.

Mitigation: Confirm the hotel, room, dates, guests, total price, guest contact details, payment method, and cancellation terms before calling create_booking; use recreate_payment_link instead of creating a duplicate booking when a payment link expires.

Risk: Booking transmits guest name, phone number, email address, booking details, payment method choice, and the user's original request text to PriceWin's backend.

Mitigation: Collect only the required booking information, avoid adding unrelated sensitive details to the original request, and ensure the guest email is typed by the user in the chat.

Risk: Users may try to provide payment credentials directly to the agent.

Mitigation: Do not ask for or accept card numbers, CVV, bank credentials, or PayPal logins; direct users to complete payment only through the returned provider payment link.

Risk: The PriceWin MCP backend and booking backend are not fully auditable from the skill artifact.

Mitigation: Install only if comfortable with PriceWin creating reservations and receiving required guest contact details; use comparison-only PriceWin skills when no transaction authority is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cotghw/skills/pricewin-booking-assistant)
- [PriceWin skills hub](https://github.com/Price-Win/pricewin-skills-hub)
- [Tool reference](artifact/reference.md)
- [Security and data handling](artifact/SECURITY.md)
- [PriceWin](https://price.win)
- [PriceWin MCP endpoint](https://mcp.price.win/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown booking recommendations and booking-management responses with tool-returned payment links, confirmation codes, and OTA links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user-approved pricewin MCP server; the skill itself ships no executable code.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
