## Description:

Recommends must-play attractions for a city by using FlyAI CLI to retrieve 5A-rated attractions and popular well-reviewed points of interest, then returns detailed travel recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysxiiun](https://clawhub.ai/user/ysxiiun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to answer city attraction questions with curated must-play recommendations, including 5A-rated sites, popular attractions, ticket notes, travel time, transit guidance, tags, images, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a broad third-party FlyAI CLI and network travel searches.

Mitigation: Use the skill only after reviewing the FlyAI CLI dependency, prefer a pinned or local CLI install, and limit agent use to attraction-related FlyAI commands.

Risk: Recommendations may include external booking links and images from FlyAI results.

Mitigation: Inspect booking URLs before opening them and treat external result content as untrusted until verified.

Risk: An optional FlyAI API key may be stored for enhanced results.

Mitigation: Avoid configuring an API key unless needed; if configured, store it with the least exposure available in the runtime environment.

## Reference(s):

- [FlyAI CLI Reference](flyai-readme.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown travel recommendation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a city name input; outputs attraction entries that may include externally sourced images and booking URLs from FlyAI results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
