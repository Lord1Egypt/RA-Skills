## Description:

Queries and analyzes public Bilibili data through the MaxHub API, covering videos, creators, search, comments, danmaku, livestreams, and public collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Bilibili creators, analysts, and researchers use this skill to look up and summarize public video, creator, search, discussion, livestream, and collection data for content planning and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the API key and user-supplied IDs, keywords, and URLs to the third-party MaxHub API.

Mitigation: Use only for authorized queries, minimize personal data, and keep the API key out of logs and prompts.

Risk: The skill documents local confirmation and audit records, as well as an API balance lookup; the security guidance flags these for review.

Mitigation: Review whether local recordkeeping and balance access are acceptable and necessary, and use a reviewed, pinned release.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-bilibili)
- [MaxHub API service](https://www.aconfig.cn)
- [SkillHub listing](https://skillhub.cn/skills/bilibili-pro)
- [Endpoint whitelist](references/endpoints_whitelist.yaml)
- [Video reference](references/video.md)
- [Creator and user reference](references/user.md)
- [Search reference](references/search.md)
- [Comments and danmaku reference](references/comments.md)
- [Livestream reference](references/live.md)
- [Collections reference](references/collections.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries, lists, and tables based on API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize public Bilibili video, creator, search, comment, danmaku, livestream, and collection data.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
