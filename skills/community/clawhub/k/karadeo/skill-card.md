## Description:

Transcribe audio or video files to time-synced lyrics or subtitle formats like LRC, SRT, WebVTT, ASS, and TTML, and create karaoke videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiqingtangx](https://clawhub.ai/user/weiqingtangx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content tooling teams use this skill to connect agents to Karadeo APIs and MCP tools for turning public audio or video URLs into timed lyric and subtitle outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media URLs and optional transcript text are sent to Karadeo for processing.

Mitigation: Use only public or approved media and avoid confidential, private, or access-controlled content unless Karadeo's handling of that data is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiqingtangx/skills/karadeo)
- [Karadeo Lyrics API documentation](https://karadeo.com/resources/karadeo-lyrics-api)
- [Karadeo OpenAPI documentation](https://karadeo.com/api/doc)
- [Karadeo MCP server card](https://karadeo.com/.well-known/mcp/server-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; API responses are plain text subtitle or lyric files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supported subtitle and lyric outputs include LRC, SRT, ASS, WebVTT, TTML, and TXT.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
