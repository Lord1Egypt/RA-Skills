## Description: <br>
Find and book real-world things to do in cities worldwide through Outgoing's natural-language search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outgoing](https://clawhub.ai/user/outgoing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover restaurants, bars, concerts, museums, accessible outings, trip activities, and other local events, then route bookable selections to Outgoing ticket booking when the user is ready to purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search prompts, city or precise-location hints, and user-linked identifiers are sent to Outgoing. <br>
Mitigation: Use a pseudonymous service-specific user ID, avoid confidential prompt details, and disclose the data flow before use. <br>
Risk: A real payment token or paid booking request can submit an actual purchase. <br>
Mitigation: Require clear user confirmation before paid bookings and use dry-run tokens when validating booking flows. <br>
Risk: The skill requires a sensitive Outgoing API credential. <br>
Mitigation: Store OUTGOING_API_KEY only as a secret environment variable and avoid exposing it in logs, prompts, or shared output. <br>
Risk: Venue details, prices, availability, and accessibility information may be incomplete or change after search results are returned. <br>
Mitigation: Report only API-returned details and ask users to confirm important access, price, and availability constraints with the venue before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/outgoing/outgoing-event-discovery) <br>
- [Outgoing developer homepage](https://www.outgoing.world/developers) <br>
- [Outgoing LLM API reference](https://www.outgoing.world/llms.txt) <br>
- [Outgoing full LLM API reference](https://www.outgoing.world/llms-full.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown guidance with curl examples and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OUTGOING_API_KEY and curl; search and booking calls may include user prompts, location hints, external user IDs, and payment tokens.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
