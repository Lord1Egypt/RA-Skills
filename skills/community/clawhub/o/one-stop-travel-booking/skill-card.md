## Description:

一站式旅行预订 provides Booking.com-style hotel search, room lookup, price comparison, and reservation-management functions for international travel planning.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users can ask an agent to search international hotels, compare room and price information, and format Booking.com-style reservation-management responses. Because the security evidence flags fabricated hotel, room, price, and review data, this should be treated as a demo until live API behavior is verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill appears to return fabricated hotel, room, price, and review data as successful results.

Mitigation: Treat outputs as demonstration content only; do not use them for real travel decisions, budgets, bookings, cancellations, or availability checks until verified live API calls replace mock data paths.

Risk: The security guidance says the description should not exceed implemented capabilities.

Mitigation: Before production use, narrow public claims to verified behavior and confirm Booking.com Affiliate API integration, credentials, and live response handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/one-stop-travel-booking)
- [Booking.com getHotels API reference](https://distribution-xml.booking.com/json/bookings.getHotels)
- [Booking.com distribution JSON API base](https://distribution-xml.booking.com/json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON objects and Markdown/text hotel tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Booking.com API credentials; current evidence flags mock hotel, room, price, and review data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
