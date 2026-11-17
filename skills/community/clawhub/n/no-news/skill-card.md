## Description:

Fetch and display international tech news from 8 curated RSS feeds with summaries, titles, links, and timestamps in a markdown table format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch a concise international technology news digest from curated RSS feeds and present it as a markdown table. It is intended for broad tech news requests, not AI-only, China-only, or Hacker News-only aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RSS article text and links come from external publishers and may contain untrusted or misleading content.

Mitigation: Review feed entries and article links before relying on or opening them.

Risk: The skill uses unpinned Python dependencies.

Mitigation: Install dependencies in a virtual environment and review dependency versions before deployment.

Risk: Fetched feed data may be cached under the user's home directory.

Mitigation: Run with --no-cache when local cached feed data should not be retained.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown table with article titles, linked sources, timestamps, and optional summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache fetched RSS feed data locally for 30 minutes unless run with --no-cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
