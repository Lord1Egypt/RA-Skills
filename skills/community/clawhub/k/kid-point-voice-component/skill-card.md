## Description: <br>
Kid Point Voice Component provides text-to-speech and speech-to-text support with automatic language-based routing across SenseAudio and Edge TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cowboy231](https://clawhub.ai/user/cowboy231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add multilingual voice output and audio transcription to a kids points or study workflow. It can generate WAV or MP3 audio, play generated speech locally, and transcribe audio through SenseAudio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TTS text and ASR audio may be sent to SenseAudio or Microsoft Edge TTS cloud services. <br>
Mitigation: Avoid sensitive recordings, secrets, regulated data, and confidential workplace content unless the relevant provider terms are acceptable. <br>
Risk: The skill can use a configured SENSE_API_KEY when calling SenseAudio. <br>
Mitigation: Configure the API key only in the intended environment and rotate or remove it if the workspace is shared or no longer trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cowboy231/kid-point-voice-component) <br>
- [SenseAudio text-to-speech API documentation](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio speech recognition HTTP API documentation](https://senseaudio.cn/docs/speech_recognition/http_api) <br>
- [SenseAudio](https://senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Command-line text output plus generated audio files and optional transcription files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audio is saved under an audio directory by date unless the caller supplies an explicit output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
