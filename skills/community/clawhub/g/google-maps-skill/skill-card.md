## Description: <br>
Uses a Bun TypeScript CLI to call Google Maps Platform APIs for geocoding, reverse geocoding, directions, place search and details, elevation, and timezone lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need command-line Google Maps queries, including address lookup, route planning, place search, elevation, and timezone data from Google Maps Platform APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps API keys may be exposed in error output, especially for query-parameter authenticated requests. <br>
Mitigation: Restrict the API key to required Google Maps APIs and approved domains, set quota and billing limits, and redact request URLs, query parameters, and API keys before logging or showing errors. <br>
Risk: Address, route, and coordinate queries can send sensitive location data to Google. <br>
Mitigation: Avoid submitting private home or work addresses and sensitive route data unless necessary, and follow the deploying organization's privacy review process. <br>


## Reference(s): <br>
- [Command Map](references/command-map.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [Raw Google Maps JSON from the CLI, with Markdown command examples in the skill references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_MAPS_API_KEY; coordinates use lat,lng order.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
