## Description: <br>
Summarize podcast episodes from Spotify, Apple Podcasts, or RSS feeds. Extracts transcripts and generates summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and podcast listeners use this skill to fetch podcast audio from supported episode or feed URLs, transcribe it with Whisper, and generate concise or detailed summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast audio is downloaded from user-provided URLs. <br>
Mitigation: Use trusted podcast, RSS, or audio URLs and review the source before execution. <br>
Risk: Transcript text may be sent to Gemini or OpenAI when the corresponding API keys are configured. <br>
Mitigation: Use --transcript-only or avoid setting LLM API keys for private, regulated, paid, or proprietary audio. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daaab/podcast-summarizer) <br>
- [Publisher profile](https://clawhub.ai/user/daaab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Markdown summary or plain text transcript, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary length can be short, medium, or long; transcript-only output is supported.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
