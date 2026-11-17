## Description:

Game Informer section RSS skill that fetches news, reviews, previews, and features feeds and formats returned items as English Markdown section lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximedogawa](https://clawhub.ai/user/maximedogawa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Game Informer headline, review, preview, and feature requests by retrieving the appropriate public RSS feeds and presenting linked story titles by section.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad gaming-news prompts may be answered specifically with Game Informer results.

Mitigation: Use this skill when Game Informer is an acceptable source, and make the source clear in responses.

Risk: The skill prefers English responses even when another language is desired.

Mitigation: Set separate localization expectations if non-English output is required.

Risk: RSS fetch failures or empty feeds can leave a section without current items.

Mitigation: Omit empty sections and state failure only when all relevant fetches fail, without inventing headlines.

## Reference(s):

- [Game Informer](https://www.gameinformer.com/)
- [ClawHub skill page](https://clawhub.ai/maximedogawa/skills/news-gameinfomer)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown with section headings and numbered linked story titles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Game Informer RSS feed items; default response lists 3-5 items per included section.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
