## Description:

今日头条数据查询助手。覆盖文章、视频、用户、评论等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, analysts, and other users can query Toutiao article, video, user, and comment data through the MaxHub API, then review concise summaries and comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query parameters sent to the MaxHub API may contain confidential or unnecessary personal information.

Mitigation: Review query parameters before sending and omit confidential or unnecessary personal information.

Risk: The security review notes that the installer version is not pinned.

Mitigation: Review the release and installation source before installing or updating the skill.

Risk: The security review reports unclear scope in some fallback instructions and invocation examples.

Mitigation: Check that the intended query and documented endpoint match before making an API request.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-toutiao)
- [MaxHub API provider](https://www.aconfig.cn)
- [API content and user reference](artifact/references/api-content-user.md)
- [API parameter mappings](artifact/references/param-mappings.md)
- [ClawHub skill page](https://clawhub.ai/xiewxx/skills/maxhub-toutiao-2)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Markdown, Guidance]

**Output Format:** [Markdown summaries, tables, and findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and keeps API key values out of output.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
