## Description: <br>
AI语音合成（文本转语音） skill that converts supplied text into a speech audio link using Juhe's text-to-speech API, with selectable voices, languages, dialects, and optional local audio download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to synthesize short text prompts into speech through Juhe's TTS service, optionally selecting a voice or language and downloading the resulting audio file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Juhe's external TTS service. <br>
Mitigation: Do not synthesize secrets or sensitive personal data unless sharing that text with Juhe is acceptable. <br>
Risk: The skill requires a Juhe API key and supports passing the key on the command line. <br>
Mitigation: Prefer a dedicated key stored in JUHE_SPEECH_KEY or a local .env file, and avoid command-line key exposure on shared systems. <br>
Risk: The skill can read input from files and write downloaded audio to a chosen output path. <br>
Mitigation: Review file paths before using --file or --output, especially when running in shared or automated workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-speech-generate) <br>
- [Juhe AI Speech Synthesis TTS API documentation](https://www.juhe.cn/docs/api/id/830) <br>
- [Juhe Data](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script output containing audio links or downloaded WAV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_SPEECH_KEY API key; accepts text up to 500 characters and can write audio files to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
