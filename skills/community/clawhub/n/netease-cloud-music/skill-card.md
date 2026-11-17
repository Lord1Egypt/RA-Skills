## Description:

Helps agents summarize public NetEase Cloud Music playlists, songs, artist pages, rankings, and interaction metrics while avoiding downloads, reverse engineering, and bulk collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to inspect public NetEase Cloud Music pages, summarize playlist and song metrics, compare artist performance over recent time windows, and scan rankings for distribution patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in personal pages may expose personal information during analysis.

Mitigation: Use logged-in context only for user-approved personal-page organization and avoid automatic interactions.

Risk: High-volume scraping or automated interaction may violate platform rules or trigger human verification.

Mitigation: Keep page access manual and low-volume, and do not use the skill for batch collection, downloads, interface reverse engineering, or bypassing controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mike47512/skills/netease-cloud-music)
- [NetEase Cloud Music](https://music.163.com/)
- [NetEase Cloud Music Toplist](https://music.163.com/#/discover/toplist)
- [NetEase Cloud Music Search](https://music.163.com/#/search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries may include song, playlist, artist, album, duration, play, favorite, comment, link, genre, language, and recency comparison fields when available from public pages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
