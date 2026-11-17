## Description:

Search YouTube videos, get channel info, fetch video details and transcripts using SkillBoss API Hub or yt-dlp fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content teams use this skill to search YouTube, inspect video and channel metadata, retrieve transcripts, and summarize or analyze transcript content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party dependencies and fallback tools.

Mitigation: Review and pin npm and Python dependencies where possible, then run the skill in an isolated environment before broader use.

Risk: API keys and transcript content may be exposed through configuration, logs, repositories, or remote processing.

Mitigation: Keep SKILLBOSS_API_KEY in environment or local configuration only, avoid committing secrets, and send transcript text to SkillBoss only when remote processing is intended.

Risk: Transcript extraction may return empty, unavailable, or auto-generated text that is not accurate enough for quotation.

Mitigation: Check transcript availability and timestamped content before analysis, and verify quotes against the source video.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/godfery-yt)
- [SkillBoss API Hub](https://skillbossai.com)
- [SkillBoss API endpoint](https://api.skillbossai.com/v1)
- [youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server)
- [Clawdbot](https://clawdbot.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YouTube metadata, transcript text with timestamps, analysis prompts, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
