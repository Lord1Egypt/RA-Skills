## Description: <br>
Searches live flight prices and schedules from Google Flights through SearchAPI.io for route, date, passenger, cabin, stop, return-flight, and booking-option lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GalDayan](https://clawhub.ai/user/GalDayan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find and compare flight options, retrieve booking-option links, and prepare ranked travel results from live SearchAPI.io responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The supplied security evidence reports that travel searches and user delivery identifiers may be saved for recurring price monitoring without a clear consent boundary. <br>
Mitigation: Use price monitoring only after explicit user consent, confirm saved searches can be deleted, and present booking links for user review rather than opening or following them automatically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/GalDayan/google-flights-search) <br>
- [SearchAPI.io signup](https://www.searchapi.io/users/sign_up) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API Calls, Guidance] <br>
**Output Format:** [JSON flight-search and booking-option results with agent-facing workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEARCHAPI_KEY; writes local search logs; round-trip searches can include return-leg details for top results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
