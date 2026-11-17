## Description:

帮助代理使用 Sparki 将比赛、活动、演讲等视频提炼为节奏更集中、适合传播的高光集锦。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and developers use this skill to guide an agent through Sparki setup, video upload, highlight-oriented prompt selection, project polling, and result download for MP4 or MOV videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uploads local videos to Sparki or a configured endpoint.

Mitigation: Use it only with videos approved for upload, require clear user consent before upload, and avoid custom --base-url values unless the endpoint is fully trusted.

Risk: API keys can be stored in the local OpenClaw configuration file.

Mitigation: Prefer SPARKI_API_KEY from the environment and protect or remove saved local configuration when it is no longer needed.

Risk: Downloaded result URLs and output paths can extend beyond the skill's declared network and file-write scope.

Mitigation: Download only from trusted HTTPS result URLs and keep outputs in the declared Sparki workspace unless the user explicitly chooses another path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fischerlam/skills/highlight-reels-zh)
- [Publisher Profile](https://clawhub.ai/user/fischerlam)
- [Sparki Homepage](https://sparki.io)
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SPARKI_API_KEY; uploads MP4/MOV videos to Sparki or a configured endpoint and downloads generated MP4 results.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, ClawHub release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
