## Description:

Fetches YouTube transcripts by video ID or URL, generates structured summaries with metadata, and can deliver summaries and full transcripts to messaging platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to summarize YouTube videos from URLs or video IDs, extract metadata and key insights, and save or share the underlying transcript when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution and weak video ID handling can expose the runtime to command or path misuse.

Mitigation: Validate YouTube video IDs strictly before execution and avoid interpolating untrusted input into shell commands.

Risk: The workflow installs and runs an unverified remote transcript dependency.

Mitigation: Pin the dependency to a reviewed version, verify its source and integrity, and rebuild only from trusted code.

Risk: Full transcripts may be uploaded to SkillBoss and sent as Telegram attachments.

Mitigation: Get explicit user consent before uploads or attachments and avoid processing sensitive or private video content.

Risk: Transcript files are saved locally in plaintext.

Mitigation: Use safer temporary-file handling, set retention limits, and delete transcript files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-summarizer)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [MCP YouTube Transcript dependency](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with metadata, bullet points, and optional plaintext transcript file guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save full transcripts locally and may attach transcript files in Telegram contexts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
