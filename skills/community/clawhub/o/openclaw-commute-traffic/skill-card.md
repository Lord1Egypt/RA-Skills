## Description: <br>
Check real-time traffic conditions for a route between two locations using TomTom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xavjer](https://clawhub.ai/user/Xavjer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users ask an agent for current commute conditions, travel time, traffic delay, route alternatives, and whether to leave now for a supplied origin and destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route origins and destinations are sent to TomTom and may reveal sensitive home, work, or travel patterns. <br>
Mitigation: Confirm origin and destination before lookup when the request is vague, and avoid using remembered private locations without explicit user confirmation. <br>
Risk: User-provided locations may be unsafe if interpolated directly into a shell command. <br>
Mitigation: Invoke the traffic helper with safely separated arguments, not by concatenating raw user text into a shell command string. <br>
Risk: Traffic results can fail or become unavailable because of missing credentials, TomTom errors, rate limits, or vague locations. <br>
Mitigation: Check that TOMTOM_API_KEY is configured, relay helper errors plainly, and ask for more specific locations when geocoding fails. <br>


## Reference(s): <br>
- [Commute Traffic ClawHub listing](https://clawhub.ai/Xavjer/openclaw-commute-traffic) <br>
- [Xavjer publisher profile](https://clawhub.ai/user/Xavjer) <br>
- [TomTom Developer Portal](https://developer.tomtom.com) <br>
- [TomTom API Response Reference](references/tomtom-api-response.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON from the helper script summarized as concise natural-language traffic guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOMTOM_API_KEY and user-provided origin and destination values.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
