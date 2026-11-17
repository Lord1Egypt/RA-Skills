## Description:

妙音AI 音乐创作助手，生成歌曲、查询任务、续写音乐、生成歌词。当用户需要 AI 作曲或音乐生成时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[phongf](https://clawhub.ai/user/phongf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the Miaoyin/Growingth music service from an agent, including song generation, task status checks, lyric generation, continuation, cover, video, WAV, and stem workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user content, task identifiers, clip identifiers, titles, and the API token to a third-party music service.

Mitigation: Use it only when the user intends to use the Miaoyin/Growingth service, keep the token private, and avoid submitting unpublished or confidential material unless the provider is trusted.

Risk: Vendor-controlled purchase, free-trial, error, and diagnostic log messages may be displayed during workflows.

Mitigation: Treat service messages and raw diagnostic logs as vendor-controlled output and review them before relying on them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phongf/skills/miaoyin-ai-music)
- [Publisher profile](https://clawhub.ai/user/phongf)
- [Miaoyin API service](https://ai.growingth.com/api-service)
- [Miaoyin API base URL](https://ai.growingth.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with JSON request and response examples, shell snippets, API call guidance, task IDs, and media links returned by the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIAOYIN_API_TOKEN and sends prompts, lyrics, titles, task IDs, clip IDs, and related music workflow data to the Miaoyin/Growingth service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
