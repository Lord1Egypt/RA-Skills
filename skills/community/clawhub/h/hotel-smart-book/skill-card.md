## Description:

多旅游平台酒店比价与订房决策助手，帮你找到最便宜的酒店并告诉你该订还是再等等，含低价日历和订房建议，多旅游平台数据直连。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to compare hotel prices across multiple travel platforms, inspect low-price date ranges, and decide whether to book now or wait. It returns hotel options, price signals, booking guidance, and booking links rather than completing purchases directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search details such as city, dates, keywords, and hotel names are sent to external proxy services.

Mitigation: Review the publisher's proxy hosts and data-handling practices before using the skill with sensitive travel plans.

Risk: An embedded shared proxy token is present in the artifact.

Mitigation: The publisher should remove the shared token and require user- or deployment-scoped credentials.

Risk: Some booking links or equal-price recommendations may favor a commission-bearing platform.

Mitigation: Treat booking recommendations as decision support, verify final prices independently, and disclose affiliate or commission behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/hotel-smart-book)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Skill homepage](https://rollinggo.store)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style natural language with hotel lists, price comparisons, date recommendations, and booking advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external booking links and platform-specific price signals.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact frontmatter reports 1.0.2 and artifact _meta.json reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
