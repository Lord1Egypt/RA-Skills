## Description: <br>
Voice Memo sends native iMessage voice bubbles using ElevenLabs TTS and BlueBubbles for users who want spoken responses instead of text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amzzzzzzz](https://clawhub.ai/user/amzzzzzzz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to convert a text response into an ElevenLabs-generated voice memo and send it as a native iMessage voice bubble through a local BlueBubbles server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real iMessages through a local BlueBubbles Private API. <br>
Mitigation: Require explicit confirmation of the recipient and message before every send, remove the hardcoded default recipient, bind BlueBubbles to localhost where possible, and use a strong BlueBubbles password. <br>
Risk: Message text is sent to ElevenLabs for text-to-speech generation. <br>
Mitigation: Avoid sending sensitive or private content unless the user has approved that disclosure, and keep the ElevenLabs API key in environment configuration rather than in prompts or source text. <br>
Risk: Broad activation or default-recipient behavior could cause unintended message delivery. <br>
Mitigation: Limit invocation to explicit voice-message requests and require the agent to confirm both the recipient and final text before executing the send script. <br>


## Reference(s): <br>
- [ElevenLabs Voice Options](references/VOICES.md) <br>
- [BlueBubbles](https://bluebubbles.app) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Audio messages] <br>
**Output Format:** [Shell command execution that generates an Opus CAF audio file and sends it as an iMessage voice bubble.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS afconvert, BlueBubbles Private API, ElevenLabs credentials, BlueBubbles credentials, and an iMessage recipient.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
