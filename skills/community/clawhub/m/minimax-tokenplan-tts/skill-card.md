## Description: <br>
Generate speech audio from text using MiniMax speech-2.8-hd with voice controls, WAV file output, and optional real-time streaming playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4833675](https://clawhub.ai/user/4833675) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to turn text into spoken audio through MiniMax TTS, either by saving WAV/MP3 output files or streaming playback during live chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles MiniMax API credentials and its setup flow can lead users to place secrets in skill files. <br>
Mitigation: Prefer temporary environment variables or command-line secret handling, and rotate any API key already stored in the skill files. <br>
Risk: The streaming playback path disables normal TLS verification. <br>
Mitigation: Avoid streaming playback until TLS verification is restored; use reviewed file generation paths for sensitive use. <br>


## Reference(s): <br>
- [MiniMax Speech T2A API Documentation](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http) <br>
- [MiniMax System Voice ID FAQ](https://platform.minimaxi.com/docs/faq/system-voice-id) <br>
- [ClawHub Skill Page](https://clawhub.ai/4833675/minimax-tokenplan-tts) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated WAV or MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, network access, MINIMAX_API_KEY, and ffplay for streaming playback.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
