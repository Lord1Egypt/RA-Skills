## Description: <br>
Search YouTube videos, get channel info, fetch video details and transcripts using SkillBoss API Hub or yt-dlp fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill to search YouTube, inspect video and channel metadata, retrieve transcripts, and analyze transcript content through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send YouTube search terms, video identifiers, URLs, and transcript text to external services. <br>
Mitigation: Use it only with content approved for those services, and confirm relevant data-handling terms before processing private, sensitive, or proprietary transcripts. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Store the key in an environment variable or local Clawdbot configuration, keep it out of source code, and avoid committing it to repositories. <br>
Risk: The skill depends on third-party YouTube tooling and transcript availability. <br>
Mitigation: Review dependency trust before installation and verify transcript accuracy before using transcript text for quotes, claims, or downstream decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/godfery-youtube) <br>
- [Publisher profile](https://clawhub.ai/user/godferylindsay) <br>
- [SkillBoss API Hub](https://skillbossai.com) <br>
- [youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, configuration examples, video metadata, and transcript text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and third-party YouTube tooling; transcript availability and accuracy depend on source video captions and external service behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
