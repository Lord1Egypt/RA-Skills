## Description: <br>
Guides an agent to generate lyrics, synthesize vocal or instrumental songs with the MiniMax API, download MP3 outputs, and merge tracks with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[838997125](https://clawhub.ai/user/838997125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to call MiniMax music APIs for lyric generation, instrumental or vocal song creation, MP3 download, and optional FFmpeg merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a built-in MiniMax API key in the release. <br>
Mitigation: Review and change credential handling before use; load the user's own key from a secure configuration path and avoid committing secrets. <br>
Risk: Prompts and lyrics are sent to MiniMax for generation. <br>
Mitigation: Warn users before sending content to MiniMax and submit only material they are permitted to share with that service. <br>
Risk: The artifact can write local lyrics and audio files and can invoke FFmpeg to merge files. <br>
Mitigation: Ask before writing or overwriting local files, constrain output paths to user-approved locations, and review merge inputs before running FFmpeg. <br>


## Reference(s): <br>
- [MiniMax Music API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/838997125/minimax-music-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/838997125) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the script can write MP3 and TXT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls MiniMax API endpoints, downloads generated audio, and can merge local MP3 files with FFmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
