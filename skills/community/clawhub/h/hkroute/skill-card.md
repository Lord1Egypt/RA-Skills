## Description: <br>
Smart public transport routing for Hong Kong with real-time bus ETAs. Queries Google Maps for transit alternatives, enriches bus legs with live arrival times, and ranks routes by effective total time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7ito](https://clawhub.ai/user/7ito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and transit assistants use this skill to plan public transport trips in Hong Kong, compare transit alternatives, and surface real-time bus arrival information when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Origin, destination, and transit query details may be sent to Google Maps and public/operator ETA services. <br>
Mitigation: Use the skill only for intended Hong Kong transit requests and disclose that routing locations are processed by external services. <br>
Risk: The required Google Maps API key could be over-permissioned or exposed through an agent runtime. <br>
Mitigation: Use a restricted Google Maps Directions API key and manage it through the agent's secret storage or environment controls. <br>
Risk: Generic travel prompts may activate the skill outside clear Hong Kong public transit scenarios. <br>
Mitigation: Limit invocation to explicit Hong Kong transit-routing requests or require clarification before running the CLI. <br>
Risk: Real-time ETA enrichment can be unavailable or stale due to operator API limitations or the local 24-hour ETA database cache. <br>
Mitigation: Present ETA availability clearly and fall back to scheduled route data when live arrival data is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/7ito/hkroute) <br>
- [hkroute source repository](https://github.com/7ito/hkroute) <br>
- [hk-bus-eta library](https://github.com/hkbus/hk-bus-eta) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance for the agent plus JSON from the bundled Node CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and GOOGLE_MAPS_API_KEY; sends route origin and destination data to Google Maps and public/operator ETA services; stores a local ETA cache under the user's home cache directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
