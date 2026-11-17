## Description:

将本地视频或平台链接转写为文字，并按自定义提示生成摘要、改写、金句、分镜或翻译内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

面向内容创作者、编辑及需要处理视频的用户，用于从本地视频或平台链接提取转写文本，并生成摘要、会议纪要、改写文案及翻译等内容。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video links can redirect to private-network data that is then uploaded to the provider; bundled code does not establish server-deletion or no-training guarantees.

Mitigation: Use only trusted links and media you are comfortable uploading to a paid provider. Isolate link processing from private network services until redirect restrictions are added, and do not rely on unverified deletion or no-training promises.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-video-transcript-fetch)
- [GuaiKei](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Transcription or prompt-shaped text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription can be cleaned and transformed according to a custom prompt.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
