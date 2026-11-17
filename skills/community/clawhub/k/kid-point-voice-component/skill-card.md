## Description:

Provides multilingual text-to-speech and speech-to-text voice utilities for a kid points workflow, using SenseAudio for Chinese and Edge TTS for English and Japanese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cowboy231](https://clawhub.ai/user/cowboy231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add voice output and speech recognition to a kid points or study assistant workflow, including automatic language-based routing between Chinese, English, and Japanese TTS engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speech text or audio may be sent to SenseAudio and, for non-Chinese TTS, Microsoft Edge TTS.

Mitigation: Avoid sensitive recordings or confidential text, and make sure users understand when cloud speech services are used.

Risk: SenseAudio access depends on SENSE_API_KEY configuration.

Mitigation: Configure the API key deliberately, restrict access to local configuration files, and rotate the key if it is exposed.

Risk: Setup and troubleshooting guidance may install Python dependencies or optional local audio players.

Mitigation: Use a virtual environment with pinned Python dependencies, and run optional sudo player-install commands only when trusted and necessary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cowboy231/skills/kid-point-voice-component)
- [SenseAudio Text-to-Speech API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Speech Recognition HTTP API](https://senseaudio.cn/docs/speech_recognition/http_api)

## Skill Output:

**Output Type(s):** [Text, Audio files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with command examples; generated WAV/MP3 audio files or plain text transcriptions from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SENSE_API_KEY for SenseAudio access and may call SenseAudio and Microsoft Edge TTS cloud services.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
