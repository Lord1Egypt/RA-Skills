## Description:

智能规划中国用户的假期旅行行程，支持法定节假日和自定义假期长度；提供目的地风土人情、景点介绍、历史故事和网红打卡地推荐；当用户需要规划旅行、了解目的地或安排假期行程时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking travelers use this skill to plan holiday trips, compare destinations, and turn holiday length, destination, party size, budget, and travel preferences into practical itineraries. It is especially oriented toward Chinese statutory holidays and custom vacation periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill assumes Chinese public holidays and Chinese-language travel-planning conventions by default.

Mitigation: Tell the agent explicitly when planning for another country, calendar, or output language.

Risk: Travel details such as transport schedules, ticket prices, restaurant availability, weather, and attraction opening hours can change.

Mitigation: Verify time-sensitive travel details with current official or booking sources before making reservations or departing.

## Reference(s):

- [中国法定节假日与常见假期参考](references/chinese-holidays.md)
- [目的地类型规划要点](references/destination-types.md)
- [行程输出模板](references/trip-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown itinerary guidance with tables and structured lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversational output may include itinerary options, booking reminders, destination background, budget estimates, and adjustment prompts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
