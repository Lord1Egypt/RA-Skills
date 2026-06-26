## Description: <br>
Download Instagram Reels, transcribe audio, and extract captions. Share a reel URL and get back a full transcript with the original description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoinedc](https://clawhub.ai/user/antoinedc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, social media analysts, and developers use this skill to turn Instagram Reel URLs into reusable transcripts and caption metadata through a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reel audio is sent to Groq for transcription. <br>
Mitigation: Only process media that is public or that you are authorized to share with Groq, and avoid private, copyrighted, or sensitive content. <br>
Risk: Instagram cookie files can function like login tokens when used for private reels. <br>
Mitigation: Use cookies only when necessary, keep cookie files local, never share or commit them, and delete them after use. <br>
Risk: Temporary metadata and audio files may remain on disk after processing. <br>
Mitigation: Remove temporary reel metadata and audio files after transcription. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/antoinedc/instagram-reels) <br>
- [Publisher Profile](https://clawhub.ai/user/antoinedc) <br>
- [Groq](https://groq.com) <br>
- [Groq Console](https://console.groq.com) <br>
- [Groq Audio Transcriptions API Endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a transcript, timestamped transcription segments, caption text, author metadata, and duration when source metadata is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
