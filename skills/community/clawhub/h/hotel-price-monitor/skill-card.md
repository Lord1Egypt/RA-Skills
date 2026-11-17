## Description:

酒店降价监控与多平台比价助手，可按城市搜索酒店、按酒店名称比较多个旅游平台的实时价格，并输出结构化价格监控请求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to compare hotel prices across travel platforms, evaluate cancellation policies, and prepare follow-up price-watch requests for selected hotels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel names, cities, dates, and occupancy details are sent through the publisher's proxy services.

Mitigation: Review the publisher and proxy data path before use, and avoid sending sensitive itinerary details unless that data sharing is acceptable.

Risk: The bundled security summary flags a hard-coded shared proxy token.

Mitigation: Rotate the shared token and move it into protected configuration before relying on the skill in a managed environment.

Risk: The security summary says the skill overstates price-monitoring behavior.

Mitigation: Treat price watching as a structured request for a host agent to handle, not as a built-in scheduler or notification service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/hotel-price-monitor)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-formatted script output and structured price-watch requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and sends hotel query parameters to proxy services for live price results.]

## Skill Version(s):

1.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
