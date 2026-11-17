## Description:

观势 — 情报获取专家 searches, fetches, extracts, and cross-checks external industry intelligence sources such as annual reports, research reports, white papers, and third-party reports, then returns structured sourced summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Strategy and research agents use this skill to collect public industry intelligence, fetch report or web page text, extract key figures, compare multiple sources, and return confidence-labeled summaries for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External industry sources may be stale, biased, paywalled, or inconsistent across reporting methods.

Mitigation: Preserve source URLs and dates, use the skill's confidence labels, mark blocked or stale sources, and review conflicts before downstream analysis.

Risk: Public web collection can cross access or privacy boundaries if used against restricted sources.

Mitigation: Use lawful public sources only, do not bypass paywalls or access controls, and substitute accessible sources when content is blocked.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown with structured JSON snippets, source URLs, dates, findings, and confidence labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve source URLs and publication dates, flag stale or blocked sources, and limit a single task to at most 10 fetched URLs unless the user confirms expansion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
