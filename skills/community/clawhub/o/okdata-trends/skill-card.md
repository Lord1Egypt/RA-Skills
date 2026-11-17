## Description:

Reads selected trending boards across seven platforms and combines rank, topic, and heat in one table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

People checking current trends use this skill to compare selected social platform boards in one table, with each topic's rank, heat, and link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign scan had medium confidence and partial coverage, so its verdict does not guarantee safety.

Mitigation: Review the skill and decide whether you trust the OKData API before installing.

Risk: Fetching trend boards incurs a charge for each platform call, including some failed calls that reach a data source.

Mitigation: Have the agent state the maximum cost before paid calls; seek approval before runs exceeding eight calls.

## Reference(s):

- [OkData trends skill guide](https://okdata.online/skills/trends/?src=skill-okdata-trends)
- [OkData 趋势技能指南](https://okdata.online/zh/skills/trends/?src=skill-okdata-trends)
- [OkData agent setup documentation](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown table with platform, rank, topic, heat, and link, followed by a brief answer, charged amount, and data source.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid board call per selected platform; states the maximum cost before calling.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
