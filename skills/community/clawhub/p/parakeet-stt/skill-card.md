## Description: <br>
Local speech-to-text with NVIDIA Parakeet TDT 0.6B v3 using ONNX on CPU, with language auto-detection and an OpenAI-compatible transcription API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlulsoe](https://clawhub.ai/user/carlulsoe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to set up and call a local speech-to-text service for transcribing audio files, producing transcripts, subtitles, timestamps, and OpenAI-compatible transcription responses without cloud APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on running an external upstream project and a local, unauthenticated speech-to-text server. <br>
Mitigation: Review or pin the upstream repository first, keep PARAKEET_URL pointed at a trusted local server, avoid exposing the port publicly without access controls, and stop the Docker service when finished. <br>


## Reference(s): <br>
- [Parakeet Stt ClawHub release](https://clawhub.ai/carlulsoe/parakeet-stt) <br>
- [Publisher profile](https://clawhub.ai/user/carlulsoe) <br>
- [Upstream Parakeet FastAPI project](https://github.com/groxaxo/parakeet-tdt-0.6b-v3-fastapi-openai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, Python snippets, configuration notes, and response format guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local API usage through PARAKEET_URL and documents text, JSON, verbose JSON, SRT, and VTT transcription outputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
