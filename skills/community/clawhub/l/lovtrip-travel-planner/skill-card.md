## Description:

Plans multi-day travel itineraries with destination checks, attraction search, budget estimation, hotel and flight assistance, and optional map links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and travel-planning agents use this skill to collect destination, duration, party, interest, and budget details, then generate itinerary plans. The skill can also guide explicit follow-up requests for weather, budgets, map links, attractions, hotels, flights, and route optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command installs a mutable third-party package using `lovtrip@latest`.

Mitigation: Pin and review a specific LovTrip package version before installation or deployment.

Risk: The skill requires API keys for external services.

Mitigation: Use dedicated low-quota keys and avoid exposing unrelated environment variables to the MCP server.

Risk: Travel details such as destination, dates, budget, companions, and preferences may be sent to external AI, map, hotel, or flight services.

Mitigation: Warn users before sharing sensitive itinerary details and avoid entering unnecessary personal information.

## Reference(s):

- [LovTrip Skill Page](https://clawhub.ai/lizhijun/skills/lovtrip-travel-planner)
- [LovTrip AI Planner](https://lovtrip.app/planner)
- [LovTrip International Planner](https://lovtrip.app/international-planner)
- [LovTrip Developer Documentation](https://lovtrip.app/developer)
- [Tool Parameter Reference](artifact/reference.md)
- [Chengdu Planning Example](artifact/examples/plan-chengdu.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON tool arguments and travel-planning links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include itinerary tables, budget estimates, route or map links, and optional hotel or flight search guidance.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
