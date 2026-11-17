## Description:

Search YouTube videos, get channel info, fetch video details and transcripts using SkillBoss API Hub or yt-dlp fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content analysts use this skill to search YouTube, retrieve channel and video metadata, collect transcripts, and optionally analyze transcript text through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable third-party tooling such as youtube-mcp-server and yt-dlp.

Mitigation: Pin dependency versions, install in a virtual environment or container, and review packages before use.

Risk: Transcript analysis examples can send full transcript text to SkillBoss API Hub.

Mitigation: Do not process private, confidential, or sensitive transcript content unless external transmission to SkillBoss is intended and approved.

Risk: The skill requires a SkillBoss API key.

Mitigation: Provide the key through environment variables or local configuration and do not commit secrets to repositories.

Risk: YouTube transcripts may be auto-generated or unavailable.

Mitigation: Review transcript accuracy before quoting or using transcript-derived analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-youtube)
- [SkillBoss API Hub](https://skillbossai.com)
- [youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server)
- [Clawdbot](https://clawdbot.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command and code examples; tool results may include video metadata, transcripts, and analysis text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can depend on external YouTube, SkillBoss API Hub, youtube-mcp-server, and yt-dlp availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
