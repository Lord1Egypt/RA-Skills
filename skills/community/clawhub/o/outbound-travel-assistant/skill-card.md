## Description: <br>
Provides outbound travel assistance for flight and hotel search, visa requirements, destination safety notes, plug and voltage guidance, tax refund estimates, exchange-rate conversion, baggage and seat information, hotel room policies, and emergency contact guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to collect outbound travel planning information, including bookings, entry requirements, local safety context, tax refunds, exchange rates, and emergency help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel-search details and an optional proxy token may be sent through the configured cloud proxy. <br>
Mitigation: Use the proxy-backed tools only when comfortable with that data flow, and do not set PROXY_TOKEN unless the proxy operator is trusted. <br>
Risk: Visa requirements, safety conditions, prices, tax refund amounts, and exchange rates can change after the skill's local data or remote result is produced. <br>
Mitigation: Confirm travel requirements, safety advisories, payments, refunds, and currency conversions with official or transaction-time sources before acting. <br>
Risk: Booking links and travel estimates may require user action and may not represent final terms. <br>
Mitigation: Review the provider's checkout page, cancellation rules, fees, and itinerary details before completing any purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/outbound-travel-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON strings and concise travel guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include booking URLs, estimates, warnings, and locally stored destination facts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
