## Description:

通过对话收集出行需求，结合可用的实时天气、地图和搜索信息，提供交通、住宿、餐饮与每日行程建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhiqiang110](https://clawhub.ai/user/pengzhiqiang110)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers use this skill to plan trips through a guided conversation, compare transport and lodging options, and receive day-by-day itineraries with estimated costs and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guide asks travelers to share weather and map API keys in ordinary chat, where their storage or exposure may be unclear.

Mitigation: Avoid pasting keys into chat unless the platform's handling is understood; use an approved secret-storage method when available.

Risk: Nearby searches may send a user's location or coordinates to map services despite disclosure focused on destination names.

Mitigation: Explain the possible location and coordinate transfer and obtain informed consent before using nearby-search features.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pengzhiqiang110/skills/lingtu-travel-planner)
- [API configuration guide](references/API_CONFIG_GUIDE.md)
- [Example itinerary](references/EXAMPLE_OUTPUT.md)
- [QWeather developer platform](https://dev.qweather.com/)
- [Amap open platform](https://lbs.amap.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational Markdown with day-by-day itineraries, estimates, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source and retrieval-time notes for changing travel information when available.]

## Skill Version(s):

7.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
