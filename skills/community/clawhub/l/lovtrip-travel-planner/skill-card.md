## Description: <br>
AI itinerary planning skill for generating multi-day travel plans with attraction search, budget calculation, hotel search, and flight search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to gather required trip details, generate itineraries, and optionally search attractions, budgets, maps, hotels, flights, weather, and route options when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external MCP package and travel services. <br>
Mitigation: Install only from trusted sources, prefer pinning a specific package version, and review MCP behavior before use. <br>
Risk: Travel details may be sent to mapping, AI, hotel, or flight services. <br>
Mitigation: Share only the trip details needed for the request and avoid entering unnecessary personal or sensitive information. <br>
Risk: AMAP and OpenRouter API keys are required for some workflows. <br>
Mitigation: Use restricted, revocable keys and avoid committing credentials to source control. <br>


## Reference(s): <br>
- [LovTrip AI Travel Planner](https://lovtrip.app/planner) <br>
- [LovTrip Developer Documentation](https://lovtrip.app/developer) <br>
- [Travel Planning Tool Parameter Reference](reference.md) <br>
- [5-Day Chengdu Planning Example](examples/plan-chengdu.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated itinerary tables, travel budget details, map links, hotel or flight search results, and route guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
