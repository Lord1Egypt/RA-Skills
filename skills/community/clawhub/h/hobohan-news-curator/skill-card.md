## Description:

Fetch, filter, dedup, and deliver curated news briefings to Telegram. Benzinga for finance, AI News RSS for tech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to receive recurring finance and AI/tech news briefings in Telegram. It searches current public news sources, filters lower-quality categories, selects important items, and formats a concise briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring Telegram delivery can expose briefing content to an external destination if private prompts or sources are added.

Mitigation: Confirm the Telegram destination and schedule before installation, and keep prompts and sources limited to public news content.

Risk: Live web search and RSS inputs can surface stale, duplicated, or low-quality news items.

Mitigation: Review source filters and briefing output periodically, and keep the documented exclusions for personal finance, crypto, forex, NFT, spam, low-quality content, price predictions, and lifestyle content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hohobohan/skills/hobohan-news-curator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted Telegram news briefing with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recurring scheduled output at 7:30am, 3:00pm, and 10:00pm; each run selects 6-8 finance and AI/tech news items.]

## Skill Version(s):

1.0.0 (source: frontmatter and changelog, released 2026-06-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
