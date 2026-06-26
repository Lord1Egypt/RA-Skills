## Description: <br>
Generates Mandarin two-host podcast scripts from topics, URLs, or PDFs, with optional persona styling and stereo TTS audio output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liaozicen666-tech](https://clawhub.ai/user/liaozicen666-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Mandarin topics, web pages, or PDFs into structured two-person podcast dialogue, Markdown transcripts, JSON session data, and optional TTS audio. It supports persona-based hosting styles and externally supplied research packages when the parent agent has web research capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled live tests may include reusable-looking credentials. <br>
Mitigation: Do not run bundled live tests with embedded credentials; use rotated credentials supplied through environment variables. <br>
Risk: PDFs, private URLs, personal documents, and derived script text may be sent to external model or TTS providers. <br>
Mitigation: Avoid confidential inputs unless the user accepts external processing, and document which providers receive content. <br>
Risk: Persona and memory data are persisted with weak scoping safeguards. <br>
Mitigation: Add path validation and provide clear procedures to view, manage, and delete saved personas and memory files. <br>
Risk: Proxy-clearing behavior may bypass expected network routing in managed environments. <br>
Mitigation: Patch or review proxy handling before use in work, sensitive, or policy-controlled environments. <br>


## Reference(s): <br>
- [Skill Instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Development Guide](DEVELOPMENT.md) <br>
- [External Research Agent](agents/external-research-agent.md) <br>
- [TTS Voice Configuration](config/tts_voices.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Audio, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown podcast dialogue, JSON session data, optional MP3 audio files, and usage guidance with Python or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can skip audio when TTS credentials are unavailable; generated files are written under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
