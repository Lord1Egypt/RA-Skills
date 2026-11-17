## Description:

Manage maps, spots, and travel plans on Ikuzo (ikuzo.app) - a location-based exploration app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordymeow](https://clawhub.ai/user/jordymeow)

### License/Terms of Use:


## Use Case:

External users use this skill to manage Ikuzo maps, saved places, and travel plans through an agent. It supports creating and editing maps, adding and searching spots, finding nearby places, and organizing day-by-day trip itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access saved maps, places, trips, and location-related account data in the connected Ikuzo account.

Mitigation: Install only when Ikuzo account access is intended, and avoid sharing sensitive current-location or private-place details unless needed.

Risk: Requests that update or delete maps, spots, or trips can change user travel-planning data.

Mitigation: Ask for scope before broad changes, specify mapIds when scope matters, and confirm destructive or trip-changing actions before execution.

## Reference(s):

- [Ikuzo Skill Page](https://clawhub.ai/jordymeow/skills/ikuzo)
- [Ikuzo MCP API](https://ikuzo.app/api/mcp)
- [Ikuzo Schema Reference](references/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, Markdown]

**Output Format:** [Markdown guidance with JSON-RPC tool call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Ikuzo account changes when connected with an authorized bearer token.]

## Skill Version(s):

2.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
