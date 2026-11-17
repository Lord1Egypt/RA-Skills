## Description:

Plans complete hiking itineraries and leader-ready route briefs for day hikes, mountain walks, coastal treks, and beginner group outings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decin](https://clawhub.ai/user/decin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trip leaders use this skill to turn hiking constraints into Chinese-language route plans, candidate trail comparisons, timing, transport, bailout options, risk notes, gear lists, cost estimates, and leader organization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hiking itinerary may be unsafe or impractical if current weather, closures, daylight, permits, transport schedules, or emergency options have changed.

Mitigation: Verify safety-critical facts from official or first-party sources before relying on the plan, especially for real-world group outings.

Risk: Unverified route distance, ascent, timing, or logistics can make a plan appear more precise than the evidence supports.

Mitigation: Label unverified details as estimates or assumptions, use conservative ranges, and ask for missing route, departure time, and group size before generating a final plan.

## Reference(s):

- [固化徒步方案输出模板](references/plan-template.md)
- [Feishu template maintenance source](https://oxktmen1w6t.feishu.cn/wiki/LC1Aw7kCUitLQckoTYxcTkJGn6f)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown route plan with itinerary, timeline, gear, weather, risk, transport, cost, and leader guidance sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed local template and labels verified, estimated, and assumed information separately.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
