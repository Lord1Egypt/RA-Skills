## Description:

Fetch and summarize recent news articles from GNews for any user-provided topic, then produce a Markdown digest with date, greeting, and top links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidk2yoyo](https://clawhub.ai/user/davidk2yoyo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate concise, linkable Markdown news digests for a user-provided topic using GNews results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GNews API key and sends user-provided topics to GNews.

Mitigation: Install only when external GNews requests are acceptable, and provide the API key through environment or dashboard configuration rather than source files.

Risk: Using --output writes a Markdown digest to the requested path.

Mitigation: Use --output only with a path the user intends to create or replace.

Risk: News summaries are limited to the articles returned by GNews and the skill's simple topic-word ranking.

Mitigation: Review linked articles before relying on the digest for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidk2yoyo/skills/noticias-cangrejo)
- [GNews](https://gnews.io/)
- [GNews Search API](https://gnews.io/api/v4/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown digest with date, Spanish greeting, topic line, and numbered article links; optional Markdown file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GNEWS_API_KEY and can request up to 20 articles, selecting up to 15 ranked links.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
