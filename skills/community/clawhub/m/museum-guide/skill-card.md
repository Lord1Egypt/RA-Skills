## Description:

Museum Guide helps visitors plan efficient museum routes, prioritize must-see artifacts, and tailor recommendations by visit length, interests, dynasty preferences, and whether children are attending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmingchen1994-dotcom](https://clawhub.ai/user/yangmingchen1994-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External museum visitors and trip planners use this skill to turn a museum name, available time, interests, and accessibility preferences into a practical visit plan with prioritized artifacts and a recommended viewing order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Museum hours, tickets, exhibit availability, and generated artifact details can be wrong, stale, or influenced by unreliable online search results.

Mitigation: Verify time-sensitive details and important exhibit claims with official museum sources before relying on the route.

Risk: Configured LLM and search providers may process museum requests, visitor preferences, and generated itinerary context.

Mitigation: Use trusted providers, prefer offline reference data where available, and avoid entering sensitive personal information.

## Reference(s):

- [China National Museum offline artifact data](references/中国国家博物馆.csv)
- [Shanghai Museum offline artifact data](references/上海博物馆.csv)
- [Palace Museum Treasure Gallery offline artifact data](references/故宫珍宝馆.csv)
- [ClawHub skill page](https://clawhub.ai/yangmingchen1994-dotcom/skills/museum-guide)
- [ClawHub publisher profile](https://clawhub.ai/user/yangmingchen1994-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON confirmation output followed by Markdown route guidance and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a two-phase flow: confirm the extracted visitor profile before generating the final route; supported museums can use offline CSV data, while other museums may require configured search and LLM services.]

## Skill Version(s):

1.4.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
