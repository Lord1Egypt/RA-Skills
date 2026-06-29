## Description: <br>
A hotel price comparison and booking decision assistant that queries multiple travel platforms, finds lower-priced hotel options, and recommends whether to book now or wait. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to compare hotel prices across travel platforms, scan flexible-date price calendars, and get booking-versus-wait guidance for a city, date range, or specific hotel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details are sent to the publisher's proxy service and onward to travel platform APIs. <br>
Mitigation: Submit only the city, dates, hotel name, and keyword needed for the comparison, and avoid adding unrelated sensitive details. <br>
Risk: Booking advice is commercial guidance and may prefer an affiliate-bearing RG link when prices tie. <br>
Mitigation: Compare the displayed platform links, prices, cancellation terms, and breakfast policies before booking. <br>
Risk: Hotel prices and platform data can change quickly or differ from the returned comparison. <br>
Mitigation: Verify the final price and policy on the booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/hotel-smart-book) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>
- [Skill homepage](https://rollinggo.store) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with CLI command examples, ranked hotel results, price calendar entries, booking links, and booking guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include live platform status, hotel prices, room policy details, booking links, and book/wait/watch signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
