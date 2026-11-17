## Description:

Queries Kuaishou video, user, search, trending, live, and comment data through the MaxHub API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Content, product, and market research teams can use the skill to retrieve Kuaishou video, creator, search, trending, live, and comment data and summarize the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags fallback from Kuaishou requests to Douyin APIs.

Mitigation: Review any cross-platform fallback and confirm the intended platform before use.

Risk: The skill sends query data to the external MaxHub service.

Mitigation: Review the data being sent to the service and avoid including sensitive information in queries.

Risk: The security guidance flags an unpinned installer.

Mitigation: Use a reviewed, exact installer version.

## Reference(s):

- [Resolved source commit](https://github.com/XieWxx/maxhub-kuaishou/commit/3c60fb9277ba0a252ba7e3d59e3db289d0365efe)
- [Source repository](https://github.com/XieWxx/maxhub-kuaishou)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-kuaishou-2)
- [MaxHub API service and key setup](https://www.aconfig.cn)
- [Video API reference](references/api-video.md)
- [User API reference](references/api-user.md)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Bilingual prose, Markdown summaries, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and summarizes retrieved API data.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
