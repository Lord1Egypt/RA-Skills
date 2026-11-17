## Description:

Kugou helps an agent inspect public Kugou Music playlists, rankings, songs, and artist pages and summarize trend, style, language, and engagement signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather concise summaries of public Kugou Music playlists, rankings, song metadata, and artist performance trends for lightweight internal analysis and reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be misused for downloads, bulk scraping, bypassing verification, or automated account-changing actions.

Mitigation: Use it only for user-directed inspection of public Kugou pages; avoid downloads, batch collection, reverse engineering, verification bypass, and automatic account interactions.

Risk: Kugou pages may be dynamically rendered or protected by human verification, which can make automated extraction incomplete or unreliable.

Mitigation: Open pages manually when needed, review what the agent reads, and treat summaries as lightweight analysis rather than authoritative records.

## Reference(s):

- [Kugou Music homepage](https://www.kugou.com/)
- [Kugou Music rankings](https://www.kugou.com/yy/rank/home/1-8888.html)
- [Kugou Music search](https://www.kugou.com/yy/html/search.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries may include song, playlist, artist, popularity, style, language, and link fields when visible on public pages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
