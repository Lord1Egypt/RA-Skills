## Description:

My Daily Brief generates a concise daily brief with Beijing weather and Baidu hot-search topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerzeng](https://clawhub.ai/user/jokerzeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get a quick China-focused daily brief with Beijing weather and current Baidu hot-search topics. It is not intended for detailed weather forecasts or in-depth news analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The schedule wording is inconsistent between the metadata and the workflow text.

Mitigation: Confirm the intended trigger time before relying on scheduled execution.

Risk: The brief is fixed to Beijing weather and Baidu hot-search results.

Mitigation: Use it for China-focused daily briefs, or edit the skill to request location and news-source preferences before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jokerzeng/skills/my-daily-brief)
- [wttr.in Beijing weather endpoint](https://wttr.in/Beijin?format=3)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown-style daily brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a weather line and a numbered list of Baidu hot-search titles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
