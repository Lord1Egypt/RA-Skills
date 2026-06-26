## Description: <br>
Manage maps, spots, and travel plans on Ikuzo (ikuzo.app) — a location-based exploration app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordymeow](https://clawhub.ai/user/jordymeow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel planners use this skill to manage Ikuzo maps, track spots, find nearby places, and build day-by-day travel itineraries through the Ikuzo API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad travel questions may trigger actions that create, update, or delete personal maps, spots, and travel plans. <br>
Mitigation: Review proposed Ikuzo API actions before changing personal travel data, especially create, update, and delete operations. <br>


## Reference(s): <br>
- [Ikuzo Skill Page](https://clawhub.ai/jordymeow/ikuzo) <br>
- [Ikuzo MCP API endpoint](https://ikuzo.app/api/mcp) <br>
- [Ikuzo Schema Reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with JSON-RPC API call details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authentication for Ikuzo API access; requested fields can be limited to reduce response size.] <br>

## Skill Version(s): <br>
2.1.3 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
