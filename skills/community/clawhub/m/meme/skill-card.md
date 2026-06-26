## Description: <br>
Create funny voice memes with various styles, effects, and templates for humorous audio content, voice memes, and social media sound clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate short comedic text-to-speech clips with preset voice effects or custom speed, pitch, and volume settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for meme generation is sent to SenseAudio for text-to-speech processing. <br>
Mitigation: Avoid submitting secrets, private personal data, or regulated content unless that data is approved for SenseAudio processing. <br>
Risk: The skill requires a SenseAudio API key for external API calls. <br>
Mitigation: Use a dedicated API key stored in SENSEAUDIO_API_KEY and apply quota controls where possible. <br>


## Reference(s): <br>
- [SenseAudio Homepage](https://senseaudio.cn) <br>
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api) <br>
- [SenseAudio API Key Console](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with Python and shell code blocks; generated audio is saved as an MP3 file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and sends selected text to the SenseAudio TTS API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
