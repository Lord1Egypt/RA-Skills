## Description: <br>
Summarize podcast episodes into concise, actionable insights from audio files, URLs, RSS feeds, and podcast platform links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hughtan93-dev](https://clawhub.ai/user/hughtan93-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and employees use this skill to turn podcast episodes into readable summaries when they want key points, detailed overviews, action items, timestamps, or related links without listening to the full audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast audio or links may contain private or sensitive content, especially when cloud transcription is used. <br>
Mitigation: Prefer local Whisper for private recordings and avoid sending sensitive audio to external APIs unless the user has approved that handling. <br>
Risk: User-supplied media URLs may point to untrusted or unexpected downloads. <br>
Mitigation: Review URLs before downloading media and process downloaded files in a controlled environment. <br>
Risk: An OPENAI_API_KEY may be exposed if configured or shared carelessly. <br>
Mitigation: Store API keys in environment variables or a secrets manager and do not commit or paste keys into summaries or logs. <br>
Risk: Installing suggested transcription and media packages can affect the local Python environment. <br>
Mitigation: Use a virtual environment for yt-dlp, Whisper, and related Python packages. <br>


## Reference(s): <br>
- [Podcast Summarize Technical Reference](references/technical.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with structured sections and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include episode metadata, key points, detailed summary, action items, timestamps, and related links when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
