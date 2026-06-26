## Description: <br>
Query real-time MBTA transit data for next departures, service alerts, live vehicle positions, stop searches, and route listings across subway, bus, commuter rail, and ferry service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squidpunch](https://clawhub.ai/user/squidpunch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents serving MBTA riders use this skill to look up real-time departures, active service alerts, live vehicle locations, stops, and routes for Boston-area transit. <br>

### Deployment Geography for Use: <br>
Global use; results are specific to the MBTA service area in Massachusetts. <br>

## Known Risks and Mitigations: <br>
Risk: Stop names, route IDs, and any configured MBTA_API_KEY may be sent to MBTA's API. <br>
Mitigation: Use a dedicated MBTA API key and avoid entering unrelated private or sensitive information. <br>
Risk: The bundled Python helper makes outbound read-only requests to MBTA's public API. <br>
Mitigation: Run it only in environments where outbound requests to api-v3.mbta.com are acceptable. <br>


## Reference(s): <br>
- [MBTA V3 API Reference](references/API.md) <br>
- [MBTA V3 API](https://api-v3.mbta.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MBTA API queries; an optional MBTA_API_KEY increases rate limits and is sent to MBTA's API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
