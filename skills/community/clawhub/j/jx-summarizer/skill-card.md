## Description: <br>
Automatically fetches YouTube video transcripts, generates structured summaries, and sends full transcripts to messaging platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to summarize YouTube videos from shared URLs and retrieve full transcript files when captions are available. It is suited for quick review of video metadata, main thesis, key insights, notable points, and takeaways. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video transcripts may contain private or sensitive information and are sent to an external summarization service. <br>
Mitigation: Avoid using the skill with private or sensitive videos unless external processing is acceptable. <br>
Risk: Full transcripts are saved locally and may be attached in Telegram chats. <br>
Mitigation: Periodically delete saved transcript files and confirm the destination chat before sending attachments. <br>
Risk: The skill depends on an external MCP transcript server. <br>
Mitigation: Inspect and pin the external dependency before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kirkraman/jx-summarizer) <br>
- [MCP YouTube Transcript dependency](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with optional transcript text file and installation or troubleshooting commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save full transcripts locally and attach transcript files in Telegram contexts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
