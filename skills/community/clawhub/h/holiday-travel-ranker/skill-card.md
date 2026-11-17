## Description:

Ranks domestic and international holiday travel destinations for Chinese public holidays using user preferences, web research, and an eight-dimension scoring model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dilicloud11](https://clawhub.ai/user/dilicloud11)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare where to travel during Chinese public holidays, based on departure city, target holiday, preferred ranking factors, and optional budget. It produces ranked destination recommendations with supporting price, visa, weather, safety, and experience evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel prices, visa policies, weather, and safety conditions can change after report generation.

Mitigation: Treat generated rankings as decision support and verify current booking prices, visa requirements, weather, and safety notices before travel.

Risk: The workflow may run several web searches and create local Markdown and HTML reports.

Mitigation: Invoke it explicitly for structured destination comparison and review generated files before sharing or relying on them.

## Reference(s):

- [Holiday Travel Ranker on ClawHub](https://clawhub.ai/dilicloud11/skills/holiday-travel-ranker)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Guidance]

**Output Format:** [Markdown report and standalone HTML page]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Top 10 domestic and international rankings, dimension-level tables, destination detail cards, and personalized recommendations.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
