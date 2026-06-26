## Description: <br>
Search YouTube videos, get channel info, fetch video details and transcripts using SkillBoss API Hub or yt-dlp fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill to find YouTube videos, inspect channels and playlists, retrieve transcripts, and summarize or analyze transcript content through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Store the key in an environment variable or scoped Clawdbot configuration, and do not commit it to source control. <br>
Risk: Transcript analysis sends content to SkillBoss API Hub. <br>
Mitigation: Redact sensitive transcript content before analysis and use the skill only where remote processing is acceptable. <br>
Risk: YouTube transcripts may be missing, empty, or auto-generated with errors. <br>
Mitigation: Use the yt-dlp fallback when MCP transcript retrieval fails and verify transcript accuracy before quoting or relying on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/godfery-yt) <br>
- [SkillBoss API Hub](https://skillbossai.com) <br>
- [youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) <br>
- [Clawdbot](https://clawdbot.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce YouTube search results, video metadata, channel or playlist details, transcript files, and transcript analysis guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
