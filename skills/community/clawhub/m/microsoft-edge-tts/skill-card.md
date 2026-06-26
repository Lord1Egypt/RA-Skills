## Description: <br>
Use Microsoft Edge online TTS service to convert text to speech. Supports command line and module invocation, no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate speech audio and subtitle files from text with Microsoft Edge's online TTS service, including voice, language, output format, rate, pitch, volume, proxy, and timeout configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text converted with this skill is sent to Microsoft Edge's online TTS service. <br>
Mitigation: Do not use it for passwords, secrets, regulated data, or confidential documents unless the data handling has been reviewed and accepted. <br>
Risk: The skill examples execute the referenced npm package with npx. <br>
Mitigation: Review and trust the package before execution, and pin or manage versions according to local dependency policy. <br>


## Reference(s): <br>
- [Microsoft Voice Support Documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of MP3 audio files and JSON subtitle files through the referenced npm package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
