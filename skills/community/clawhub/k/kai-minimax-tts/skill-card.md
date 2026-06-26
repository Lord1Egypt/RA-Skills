## Description: <br>
Generate voice audio and transcribe speech using MiniMax TTS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate English or Spanish speech audio through MiniMax and to transcribe local audio files into text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text provided for speech generation is sent to MiniMax. <br>
Mitigation: Avoid sending secrets, regulated content, or sensitive personal data unless that use is approved. <br>
Risk: Generated audio and transcript files are saved locally and may contain sensitive content. <br>
Mitigation: Use an appropriate workspace location and delete generated files when they are no longer needed. <br>
Risk: The skill depends on a MiniMax API key and local command-line tools. <br>
Mitigation: Keep MINIMAX_API_KEY protected and confirm whisper, curl, and xxd are installed before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ogdegenblaze/kai-minimax-tts) <br>
- [MiniMax text-to-audio API endpoint](https://api-uw.minimax.io/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown instructions with shell commands; generated MP3 audio and TXT transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY plus whisper, curl, and xxd; writes Kai.mp3 and latest_from_blaze.txt in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
