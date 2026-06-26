## Description: <br>
MiniMax speech synthesizes text to audio, manages asynchronous TTS tasks, and supports voice cloning, voice design, voice lookup, and voice deletion through the MiniMax API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silingyuan0](https://clawhub.ai/user/silingyuan0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate speech audio files from text, submit and query asynchronous TTS jobs, and manage MiniMax voices for cloning, design, lookup, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text and selected audio are sent to MiniMax APIs for synthesis, cloning, or voice design. <br>
Mitigation: Use a dedicated MiniMax API key where possible and send only text and audio that are approved for processing by MiniMax. <br>
Risk: Voice cloning can process uploaded reference audio and create reusable voice IDs. <br>
Mitigation: Upload only voices that the user has permission to clone and check MiniMax review requirements before using cloned or designed voices. <br>
Risk: The delete command removes a MiniMax voice by voice ID and the skill does not add a separate confirmation step. <br>
Mitigation: Double-check the target voice ID before running deletion commands. <br>


## Reference(s): <br>
- [MiniMax speech API reference](artifact/references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/silingyuan0/minimax-speech-generate) <br>
- [MiniMax China API endpoint](https://api.minimaxi.com/v1) <br>
- [MiniMax international API endpoint](https://api.minimax.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, API Calls] <br>
**Output Format:** [Markdown guidance, Python functions, CLI commands, JSON API responses, and local audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces mp3, wav, or pcm audio files; may return MiniMax task IDs, voice IDs, base64 audio, or JSON status data.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
