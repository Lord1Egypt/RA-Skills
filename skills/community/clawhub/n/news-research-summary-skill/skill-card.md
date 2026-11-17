## Description:

Researches news and factual information on the web, then produces a cited, deduplicated summary tailored to constraints such as topic, time range, region, sources, language, length, and angle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinouyang](https://clawhub.ai/user/darinouyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, product teams, and developers use this skill to research current news, policy updates, competitor activity, industry developments, and factual topics, then receive concise cited summaries with source lists and search notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on web search, so summaries can reflect stale, incomplete, conflicting, or single-source information.

Mitigation: Prioritize primary and reputable sources, corroborate key claims with independent sources when possible, cite discrepancies, and label single-source claims clearly.

Risk: The default output template uses Chinese headings and may not match every installer's preferred language.

Mitigation: Review the output language preference at installation or use time and ask the agent to match the user's language when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darinouyang/skills/news-research-summary-skill)
- [Web research and summarization reference](artifact/reference.md)
- [Example prompts and outputs](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with cited bullets, details, optional impact assessment, source list, and search notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Factual claims should include source links; unsupported analysis should be labeled as analysis, judgment, or speculation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
