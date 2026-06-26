## Description: <br>
ElevenLabs Text-to-Speech API for high-quality speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate speech audio from text with the ElevenLabs API, including handling long documents by chunking text and combining MP3 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for conversion is sent to ElevenLabs for processing. <br>
Mitigation: Use only text approved for external processing and avoid secrets, confidential documents, personal data, or regulated content unless the provider terms and data handling have been approved. <br>
Risk: The skill requires an ElevenLabs API key. <br>
Mitigation: Provide the API key through the ELEVENLABS_API_KEY environment variable and avoid hard-coding or logging the credential. <br>
Risk: ElevenLabs usage can be affected by subscription rate limits, quotas, retention terms, and billing. <br>
Mitigation: Check the active ElevenLabs plan terms before use, cache generated audio where appropriate, and monitor quota or billing impact. <br>
Risk: Long text must be split across requests, which can create awkward cuts or missing content if chunking is poor. <br>
Mitigation: Split long documents at sentence boundaries, verify generated chunks, and concatenate reviewed audio outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lnj22/pg-essay-to-audiobook-elevenlabs-tts) <br>
- [ElevenLabs Text-to-Speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id}) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, JSON, HTTP endpoint, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MP3 audio files when the example code is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
