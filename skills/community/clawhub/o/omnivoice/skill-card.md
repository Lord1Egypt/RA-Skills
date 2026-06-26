## Description: <br>
OmniVoice is an all-in-one voice identity toolkit for speaker identification, voice library management, voice cloning, speech-to-text, voice swap, and persona voice replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangqibin-caibi](https://clawhub.ai/user/yangqibin-caibi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use OmniVoice to process voice or audio requests: identify speakers from a voice library, transcribe audio, manage reference voices, clone authorized voices, and create voice-based replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples and transcripts can contain sensitive personal data. <br>
Mitigation: Use the skill only with voices and audio the user is authorized to process, store references intentionally, and delete voice-refs and TOOLS.md entries when no longer needed. <br>
Risk: Voice cloning or message-sending workflows can send selected audio or generated speech to external services. <br>
Mitigation: Use approved SiliconFlow and Feishu credentials, protect API keys, and avoid sending sensitive audio unless the user has consent and the service is acceptable for the data. <br>
Risk: Generated voice messages could be sent to the wrong Feishu recipient. <br>
Mitigation: Verify recipient IDs and credential scope before running the Feishu send script. <br>


## Reference(s): <br>
- [Voice Library Format](references/voice-library-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yangqibin-caibi/omnivoice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Audio files] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, transcripts, speaker-match results, and generated audio paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided audio and may require local voice references plus SF_API_KEY or Feishu credentials for cloning or message sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
