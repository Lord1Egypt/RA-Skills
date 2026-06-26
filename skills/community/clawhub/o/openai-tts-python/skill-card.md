## Description: <br>
Text-to-speech conversion using OpenAI's TTS API for generating natural-sounding audio from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merend](https://clawhub.ai/user/merend) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and end users use this skill to convert provided text, files, or stdin into speech audio with selectable OpenAI voices, model quality, speed, and output format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to OpenAI. <br>
Mitigation: Use the skill only for content your OpenAI account and data policies allow, and avoid secrets, regulated data, or confidential documents unless explicitly approved. <br>
Risk: The skill uses an OpenAI API key and may incur usage charges. <br>
Mitigation: Confirm API key scope, billing expectations, and request volume before batch or long-text generation. <br>
Risk: Broad activation keywords could trigger text-to-speech behavior when audio output was not intended. <br>
Mitigation: Invoke the skill only on explicit text-to-speech requests and review the text before conversion. <br>


## Reference(s): <br>
- [OpenAI TTS Documentation](https://platform.openai.com/docs/guides/text-to-speech) <br>
- [OpenAI API Reference - Create Speech](https://platform.openai.com/docs/api-reference/audio/createSpeech) <br>
- [OpenAI Pricing](https://openai.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell examples; generated audio files from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports mp3, opus, aac, and flac output; long text is split into 4096-character chunks when optional audio dependencies are available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
