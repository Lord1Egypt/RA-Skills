## Description: <br>
Multi-platform hotel price comparison and booking-decision assistant that searches hotel prices, scans low-price dates, and advises whether to book or wait. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare hotel prices across multiple travel platforms, identify cheaper stay dates, and get booking-timing guidance. It can return booking links, but users complete purchases on external travel platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details are sent through the publisher's proxy service before travel platform results are returned. <br>
Mitigation: Install only when this data flow is acceptable, and avoid entering sensitive personal information beyond the query details needed for hotel search. <br>
Risk: Booking links may reflect an undisclosed commission preference. <br>
Mitigation: Compare final prices, cancellation terms, meal inclusions, and policies directly on the travel platforms before booking. <br>
Risk: The skill's booking advice is based on platform data and heuristics, not a guarantee of future prices or availability. <br>
Mitigation: Treat book-or-wait signals as decision support and verify current prices and terms before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/hotel-smart-book) <br>
- [Skill homepage](https://rollinggo.store) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON responses with hotel listings, prices, booking links, low-price calendar entries, and booking advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include platform names, cancellation and breakfast details, prices, URLs, decision signals, confidence scores, reasons, and user-facing tips.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
