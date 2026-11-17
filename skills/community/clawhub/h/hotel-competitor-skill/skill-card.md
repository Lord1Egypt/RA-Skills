## Description:

Generates basic hotel competitor analysis reports from manual or Excel-supplied competitor data; the packaged script does not implement the advertised automatic competitor discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu65-tech](https://clawhub.ai/user/chaoliuzhu65-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel operators, regional managers, and hotel groups can use this skill to produce basic competitor reports from supplied competitor names or Excel data, including counts, ratings, price ranges, and nearby-competitor indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises automatic competitor discovery, but the packaged script only performs basic reporting from supplied data.

Mitigation: Use it only for manual or Excel-based competitor reporting unless automatic discovery is separately reviewed and implemented.

Risk: Excel input and generated Markdown may contain untrusted or misleading content.

Mitigation: Run the skill only on trusted Excel files or manually entered data, and review generated Markdown before sharing.

Risk: Dependency constraints are broad and may install newer package versions than originally tested.

Mitigation: Pin or review dependencies before installation in production environments.

## Reference(s):

- [Amap developer documentation](https://lbs.amap.com/)
- [ClawHub skill listing](https://clawhub.ai/chaoliuzhu65-tech/skills/hotel-competitor-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated from manually entered or Excel-imported competitor data; automatic fetching is skipped unless separately implemented and configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
