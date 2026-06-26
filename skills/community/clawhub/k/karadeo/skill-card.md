## Description: <br>
Transcribe audio or video files to time-synced lyrics or subtitle formats like LRC, SRT, WebVTT, ASS, and TTML, and create karaoke videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiqingtangx](https://clawhub.ai/user/weiqingtangx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to Karadeo's authenticated MCP and REST APIs for transcription, lyric alignment, subtitle generation, and karaoke video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Karadeo API keys can be exposed if pasted into shared chats, logs, or files. <br>
Mitigation: Use a dedicated, revocable API key when possible and avoid storing real keys in shared prompts or artifacts. <br>
Risk: Submitted media URLs and optional transcript text may contain private or sensitive content. <br>
Mitigation: Submit only media and transcript text that the user is authorized and comfortable sending to Karadeo's service. <br>
Risk: The REST transcription flow expects a publicly accessible media URL, which can broaden access to private media if handled carelessly. <br>
Mitigation: Prefer temporary, scoped media URLs and revoke or expire them after the transcription workflow completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weiqingtangx/karadeo) <br>
- [Karadeo dashboard](https://karadeo.com/dashboard) <br>
- [Karadeo lyrics API documentation](https://karadeo.com/resources/karadeo-lyrics-api) <br>
- [Karadeo OpenAPI documentation](https://karadeo.com/api/doc) <br>
- [Karadeo MCP server card](https://karadeo.com/.well-known/mcp/server-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward Karadeo API calls that can return subtitle or lyric text in formats such as LRC, SRT, ASS, WebVTT, TTML, or TXT.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
