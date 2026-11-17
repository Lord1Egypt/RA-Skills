## Description:

Multi-person meetup planner for recommending fair meeting venues, coordinating schedules, generating plans, and exporting map or calendar links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to plan multi-person meetups in mainland China by finding shared availability, matching interests, selecting a fair venue, and producing an itinerary with navigation or calendar outputs.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The setup example installs an external LovTrip MCP package using `@latest`, which can change between installs.

Mitigation: Use a pinned, reviewed package version before deploying the skill in a shared or production agent environment.

Risk: The skill handles participant locations, schedules, names, and calendar details that may be sensitive.

Mitigation: Collect participant consent, share only the minimum needed data, and prefer coarse locations unless exact coordinates are required.

Risk: `AMAP_API_KEY` is required for location services.

Mitigation: Store the API key in a secret manager or private environment and avoid committing it to skill files or chat transcripts.

Risk: Venue and travel recommendations are limited to mainland China and depend on city and map data quality.

Mitigation: Require the `city` parameter, verify candidate venues before finalizing plans, and use backup plans when weather, traffic, or venue availability changes.

## Reference(s):

- [LovTrip Meetup Planner on ClawHub](https://clawhub.ai/lizhijun/skills/lovtrip-meetup)
- [LovTrip Global Planner](https://lovtrip.app/global-planner)
- [LovTrip Developer Documentation](https://lovtrip.app/developer)
- [Tool Parameter Reference](artifact/reference.md)
- [Meetup Planning Example](artifact/examples/plan-meetup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated itinerary text, venue recommendations, map links, and calendar export content.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
