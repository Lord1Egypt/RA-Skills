## Description:

Helps agents fetch MediaBias.news stories, coverage splits, framing analysis, and outlet bias or factuality ratings through the free read API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fspecii](https://clawhub.ai/user/fspecii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer news and media-source questions with MediaBias.news story data, outlet ratings, coverage distribution, framing comparison, ownership details, and required citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News queries, outlet names, domains, and article URLs may be sent to MediaBias.news for analysis.

Mitigation: Install in a project-scoped context when tighter control is needed over when the skill is available.

Risk: If MediaBias.news is unavailable, the skill cannot perform the requested lookup.

Mitigation: State that the check did not run and avoid guessing outlet leanings or story analysis from memory.

Risk: Coverage percentages, blindspot findings, and outlet ratings can be misleading without attribution or denominator context.

Mitigation: Link canonical MediaBias.news pages, quote denominators for distribution data, and attribute outlet ratings to the individual rater.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fspecii/skills/media-bias-news-skill)
- [Server-Resolved GitHub Import](https://github.com/fspecii/media-bias-news-skill)
- [MediaBias.news](https://mediabias.news)
- [MediaBias.news API Discovery](https://mediabias.news/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and text responses with optional inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should attribute MediaBias.news, link canonical pages, and keep third-party outlet ratings separated by rater.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
