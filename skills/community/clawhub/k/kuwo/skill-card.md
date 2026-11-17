## Description:

Retrieves and summarizes trending public playlists, songs, and artist metrics from Kuwo Music for lightweight analysis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect public Kuwo Music playlists, charts, songs, and artist pages, then summarize engagement metrics and style or language distributions for internal analysis and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to browse and summarize Kuwo Music pages that are dynamically rendered or protected by platform controls.

Mitigation: Keep activity limited to public pages or explicitly requested personal-page organization, open dynamic pages manually when needed, and do not bypass platform controls.

Risk: Music-platform analysis can drift into downloads, bulk scraping, account actions, or use of non-public data.

Mitigation: Avoid downloads, bulk collection, automated account interactions, and non-public content; use results only for lightweight internal analysis and notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike47512/skills/kuwo)
- [Kuwo Music homepage](https://www.kuwo.cn/)
- [Kuwo Music ranking page](https://www.kuwo.cn/rankList)
- [Kuwo Music search page](https://www.kuwo.cn/search/list)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and structured metric descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links, public engagement counts, time-window comparisons, and style or language distribution summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
