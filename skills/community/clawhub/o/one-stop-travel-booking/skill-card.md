## Description: <br>
一站式旅行预订 helps agents search international hotels, compare rooms and prices, and prepare Booking.com-style reservation management responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel assistants and end users use this skill to search international hotels, compare room availability and prices, and manage Booking.com-style reservation workflows through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present mock hotel, room, price, review, cancellation, or reservation data as successful live results. <br>
Mitigation: Do not rely on it for real availability, prices, taxes, reviews, cancellation terms, bookings, or cancellations until the publisher replaces mock data with verified Booking.com API calls. <br>
Risk: Booking and cancellation flows can affect travel plans and personal data. <br>
Mitigation: Add explicit user confirmation and privacy safeguards before any booking or cancellation action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryan-zry/one-stop-travel-booking) <br>
- [Booking.com Distribution API JSON endpoint](https://distribution-xml.booking.com/json) <br>
- [Booking.com getHotels endpoint](https://distribution-xml.booking.com/json/bookings.getHotels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style function call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Booking.com API credentials; evidence indicates mock data must be replaced before real booking use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
