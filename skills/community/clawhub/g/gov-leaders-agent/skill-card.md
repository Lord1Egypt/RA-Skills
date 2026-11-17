## Description:

Collects, maintains, queries, and summarizes publicly released information about government officials across national, provincial, and local levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to gather, update, query, and produce structured reports from public government leadership information while preserving source URLs and update dates.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can crawl and store public government-official information, which could lead to collection of non-public personal details if configured too broadly.

Mitigation: Configure implementations to use only official or otherwise public sources, preserve source URLs and update dates, and exclude non-public personal details.

Risk: Personnel data may become stale or uncertain as government leadership changes.

Mitigation: Include source URLs and update dates in outputs, mark uncertain information as pending confirmation, and refresh records from public sources before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/gov-leaders-agent)
- [Publisher profile](https://clawhub.ai/user/golngod)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with source URLs and update dates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include leadership lists, personnel-change notices, query answers, and summary reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
