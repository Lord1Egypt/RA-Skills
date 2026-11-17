## Description:

西瓜视频数据查询助手。覆盖视频详情、用户数据、搜索、评论等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese- and English-speaking users and content teams use the assistant to query Xigua video and creator data, including search, video details, comments, playback links, profiles, and posts, then review or compare the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video-query fallbacks may send requests to Douyin endpoints outside the stated Xigua scope.

Mitigation: Review endpoint targets and restrict outbound requests to the services approved for the intended Xigua queries.

Risk: The documented installation command is unpinned, so the installed release may change over time.

Mitigation: Install a reviewed, version-pinned release and inspect its contents before use.

Risk: The security analysis is incomplete because two local references were unresolved.

Mitigation: Resolve and review the referenced files, then repeat the security scan before relying on the assessment.

## Reference(s):

- [Video and user API reference](references/api-video-user.md)
- [Parameter mappings](references/param-mappings.md)
- [MaxHub website and API service](https://www.aconfig.cn)
- [Server-resolved source repository](https://github.com/XieWxx/maxhub-xigua)
- [ClawHub skill release](https://clawhub.ai/xiewxx/skills/maxhub-xigua-2)
- [Publisher profile](https://clawhub.ai/user/xiewxx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Chinese or English Markdown with summaries, lists, and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language follows the user; findings are based on returned API data, with human-readable number formatting.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
