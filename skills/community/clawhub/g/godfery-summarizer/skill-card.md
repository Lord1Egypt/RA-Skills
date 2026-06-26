## Description: <br>
Fetches YouTube transcripts by video ID or URL, generates structured summaries with metadata, and delivers summaries and full transcripts to messaging platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
End users and agent operators use this skill to summarize or transcribe YouTube videos. It returns a structured summary and, when supported by the channel, saves or delivers the full transcript as a text file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full YouTube transcripts may be sent to SkillBoss for summarization and included in messaging-platform contexts. <br>
Mitigation: Use the skill only for content that is approved for external processing, and avoid submitting private or sensitive transcript content. <br>
Risk: The skill can install and run an unpinned third-party transcript server. <br>
Mitigation: Review and pin the transcript server dependency before installation, and run the skill in a contained environment. <br>
Risk: Full transcripts can be saved on the host without a clear retention policy. <br>
Mitigation: Define a deletion policy for saved transcript files and limit filesystem access to the transcript directory. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/godferylindsay/godfery-summarizer) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [MCP YouTube Transcript server](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary, transcript text file, and optional messaging-platform file attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses transcript metadata when available and may save full transcripts under /root/clawd/transcripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
