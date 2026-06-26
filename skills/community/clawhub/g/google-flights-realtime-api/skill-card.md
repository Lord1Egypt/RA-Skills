## Description: <br>
Search Google Flights for real-time one-way and round-trip flight deals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtnrabi](https://clawhub.ai/user/mtnrabi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search one-way or round-trip flights, compare prices and timings, and filter results by stops, airline, seat class, dates, and budget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad date-range or multi-destination searches can send many requests and consume paid RapidAPI quota. <br>
Mitigation: Confirm the request count before large searches and batch requests within the user's RapidAPI plan limits. <br>
Risk: Flight searches send origins, destinations, dates, filters, and a RapidAPI key to the RapidAPI-backed flight service. <br>
Mitigation: Use the skill only when sharing those travel details with the service is acceptable, and keep the RapidAPI key in the configured environment or skill secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtnrabi/google-flights-realtime-api) <br>
- [Google Flights Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/google-flights-live-api) <br>
- [Google Flights Live API pricing](https://rapidapi.com/mtnrabi/api/google-flights-live-api/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown summaries with inline curl commands and structured flight-result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAPIDAPI_KEY and outbound network access to the RapidAPI Google Flights Live API.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
