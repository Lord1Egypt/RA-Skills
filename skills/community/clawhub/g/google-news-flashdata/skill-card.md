## Description:

Search Google News with FlashData for article headlines, publishers, publication labels and links. Use for topic research, company news, news search by country or language, and preparing news digests. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find coverage of topics, companies, or events and prepare sourced briefings or digests with linked headlines, publishers, and publication labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests send the required FlashData API key and query to its hosted service, and data queries consume paid Credits.

Mitigation: Keep the key in protected secret settings and review the expected query count and credit budget before running.

Risk: The security verdict is benign, but the evidence is incomplete because Skillspector coverage was partial and two local references could not be resolved.

Mitigation: Review the documented FlashData requests and consider whether you trust the service before installing.

## Reference(s):

- [Google News source documentation](https://flashdata.dev/docs/sources/google_news?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_news-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_news-task)
- [Get a FlashData API key](https://flashdata.dev/signup?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_news-task)
- [ClawHub release page](https://clawhub.ai/flashdatadev/skills/google-news-flashdata)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON search results; optional Markdown briefings or source lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article results include headlines, publisher names, article links, publication labels, and may include snippets.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
