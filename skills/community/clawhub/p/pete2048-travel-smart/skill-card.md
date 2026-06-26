## Description: <br>
TravelSmart helps drivers choose highway exits, midway hotels, and taxi pickup points by scoring distance, ratings, detour, price, and route fit with Amap data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pete2048](https://clawhub.ai/user/pete2048) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External drivers and travel-planning agents use this skill to compare route-aware options for highway exit stops, midway lodging, and parking-to-taxi transfer points. Developers can run it through the CLI, local web API, or Feishu integration when the required map service credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web server includes an unauthenticated Feishu message relay outside the core travel-planning use case. <br>
Mitigation: Review server.py before running the web server, remove or protect /notify, and bind only to localhost unless intentional exposure is required. <br>
Risk: Travel queries can include home, hotel, itinerary, or precise location details that may be sent to configured map or LLM providers. <br>
Mitigation: Avoid entering sensitive travel details unless the configured providers and credentials are approved for that data. <br>
Risk: A default Feishu chat identifier or over-broad Feishu permissions could route notifications to an unintended destination. <br>
Mitigation: Set FEISHU_CHAT_ID explicitly and limit Feishu app permissions to the minimum required scope. <br>


## Reference(s): <br>
- [TravelSmart PRD](references/PRD.md) <br>
- [TravelSmart API Reference](references/api-reference.md) <br>
- [TravelSmart Scoring Algorithm](references/scoring-algorithm.md) <br>
- [TravelSmart ClawHub Release](https://clawhub.ai/pete2048/pete2048-travel-smart) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, CLI text, or JSON API responses with ranked travel recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_KEY for map data; MiniMax and Feishu credentials are optional.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
