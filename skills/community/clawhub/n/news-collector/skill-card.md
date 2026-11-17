## Description:

News Collector helps an agent generate personalized information briefs, either on demand or on a recurring schedule, by searching, filtering, organizing, and formatting source material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winsaney](https://clawhub.ai/user/winsaney)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure topics, source preferences, cadence, and templates for personalized news or research briefs. It supports one-time brief generation and recurring newsletter workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Periodic brief mode may browse external sites and repeatedly collect items from configured topics and sources.

Mitigation: Before enabling periodic mode, confirm the source list, collection frequency, delivery channel, and whether source lists or collected items may be saved.

Risk: Generated briefs can surface inaccurate, outdated, or low-quality material if the selected sources or filters are weak.

Mitigation: Prioritize high-quality sources, require source links for traceability, and review generated briefs before relying on them.

## Reference(s):

- [Basic Newsletter Template](assets/template-basic.md)
- [Advanced Newsletter Template](assets/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text newsletter briefs with source links and configurable sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include source lists, cadence settings, brief templates, summaries, and extended-reading links.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
