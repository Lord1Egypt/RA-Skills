## Description:

出境游一站式全链路助手，11个工具覆盖国际机票酒店搜索、签证查询、安全评级、插头电压、退税计算、汇率换算、航班座位行李、紧急求助，零配置即装即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel planners use this skill to prepare outbound trips by checking flights, hotels, visa requirements, safety context, plug standards, tax refund estimates, exchange rates, baggage, seat information, and emergency contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight, hotel, seat, baggage, and hotel-detail queries are sent to the skill's RG cloud proxy, and currency codes are sent to a public exchange-rate API.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering unnecessary personal details beyond the itinerary fields needed for a lookup.

Risk: Visa rules, destination safety conditions, tax refund amounts, travel prices, and exchange rates can change or may be estimates.

Mitigation: Confirm important decisions with official consulates, carriers, hotels, tax refund providers, emergency services, or current public sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/outbound-travel-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON-formatted Chinese text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live travel lookup results, local reference data, disclaimers, and suggested follow-up tool tips.]

## Skill Version(s):

1.0.19 (source: server release evidence and target metadata; artifact _meta.json lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
