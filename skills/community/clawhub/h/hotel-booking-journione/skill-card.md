## Description:

Search and book hotels through TourMind using live hotel, room-rate, availability, policy, order, and payment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaduzhu-ai](https://clawhub.ai/user/kaduzhu-ai)

### License/Terms of Use:

MIT

## Use Case:

External travelers, travel agents, and hospitality teams use this skill to search live hotel inventory, compare verified room rates and policies, and complete booking, payment, cancellation, or order lookup through TourMind after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide reusable TourMind tokens through chat and stores them locally as plaintext.

Mitigation: Use a minimally scoped token when available, avoid sharing tokens in logs or screenshots, restrict local token-file access, and remove skill_token.txt when the booking workflow is complete.

Risk: The skill can create bookings, start payments, cancel orders, and perform other actions with real travel and payment consequences.

Mitigation: Before confirmation, verify hotel, dates, price, taxes and fees, cancellation terms, guest name, email, payment method, and any Stripe processing fee disclosures.

Risk: Hotel prices, availability, policies, and order status depend on live TourMind API responses.

Mitigation: Use returned TourMind data as authoritative, recheck the selected rate before booking, and report API failures instead of substituting unsourced hotel or pricing information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaduzhu-ai/skills/hotel-booking-journione)
- [TourMind Booking API and Field Reference](references/parameter_guide.md)
- [TourMind Booking Skills Product Page](https://tourmind.com/skills)
- [TourMind API Base URL](https://api.tourmind.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown hotel search, booking, payment, cancellation, and order-status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TourMind result links and booking or payment status; should not expose stored tokens.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter metadata.version is 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
