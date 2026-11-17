## Description:

Provides summaries and analysis of public short videos and topics from Kuaibao/QQ Kandian for keyword, account, and trending list data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and internal operations users can use this skill to summarize public Kuaibao/QQ Kandian short-video topics, account pages, and trend lists for lightweight monitoring and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated public-page collection could exceed platform expectations or include content outside the intended public scope.

Mitigation: Keep request volume low, use only public pages, avoid login-only or private content, and follow the platform rules stated by the skill.

Risk: Dynamic rendering and human verification pages can lead to incomplete or stale extracted metrics.

Mitigation: Open pages manually when needed, verify extracted engagement metrics against the displayed source page, and include source links in summaries.

Risk: The workflow could be misused for downloading videos, reverse engineering interfaces, or bypassing platform controls.

Mitigation: Do not download media, call private interfaces, reverse engineer APIs, bypass controls, or perform bulk scraping.

## Reference(s):

- [Kuaibao homepage](https://kuaibao.qq.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/kuaibao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries with source links and public engagement metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles, author names, publish times, likes, comments, favorites, topic labels, collection times, and source links when available from public pages.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
