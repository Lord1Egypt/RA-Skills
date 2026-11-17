## Description:

Light Chaser helps travelers plan photography outings by turning destination, travel date, camera equipment, weather, and attraction research into an executable shooting timeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccshen722](https://clawhub.ai/user/ccshen722)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel photographers use this skill to plan where, when, and how to shoot during a trip, including attraction selection, weather-aware timing, device-specific shooting suggestions, route ordering, styling, and post-processing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured QWeather API key could be exposed through local configuration handling or agent output.

Mitigation: Keep config.env private, use a low-privilege QWeather key with quotas, and review outputs before sharing logs or plans.

Risk: Destination and travel-date details may be sent to weather or search services during planning.

Mitigation: Use the skill only with travel details appropriate for those services and verify the configured QWeather host is legitimate before enabling API calls.

## Reference(s):

- [Light Chaser ClawHub Skill Page](https://clawhub.ai/ccshen722/skills/light-chaser)
- [QWeather Developer Platform](https://dev.qweather.com/)
- [DJI Fly Safe](https://www.dji.com/cn/flysafe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown travel photography plan with weather summary, shooting timeline, location recommendations, equipment guidance, styling suggestions, and editing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use QWeather API data when configured; otherwise may rely on web search for lower-precision weather information.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
