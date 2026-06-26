## Description: <br>
智能规划中国用户的假期旅行行程，支持法定节假日和自定义假期长度；提供目的地风土人情、景点介绍、历史故事和网红打卡地推荐；当用户需要规划旅行、了解目的地或安排假期行程时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan holiday trips for Chinese travelers by collecting dates, destination, traveler count, budget, transportation, lodging, food, and accessibility preferences. The skill produces destination guidance and day-by-day itineraries with pacing, transport, meal, lodging, ticket, and booking reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel prices, tickets, schedules, opening hours, and availability may change after an itinerary is generated. <br>
Mitigation: Independently verify live prices, tickets, schedules, and opening hours with official providers before booking or traveling. <br>
Risk: Trip planning conversations can involve sensitive personal or payment information. <br>
Mitigation: Avoid sharing passport numbers, ID numbers, payment details, account credentials, or other sensitive identifiers. <br>
Risk: Generated itineraries and destination recommendations may not fully match traveler health, accessibility, budget, weather, or crowd constraints. <br>
Mitigation: Review the plan before relying on it, adjust pacing and constraints, and confirm suitability for all travelers. <br>


## Reference(s): <br>
- [中国法定节假日与常见假期参考](references/chinese-holidays.md) <br>
- [目的地类型规划要点](references/destination-types.md) <br>
- [行程输出模板](references/trip-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown itineraries, destination guidance, tables, checklists, and follow-up questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only conversational output; no code execution, credentials, or privileged access requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
