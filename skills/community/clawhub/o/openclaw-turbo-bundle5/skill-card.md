## Description: <br>
Integrates Groq and OpenRouter models with smart free-ride optimization and bilingual Saudi Arabic/English text-to-speech for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rvigoo](https://clawhub.ai/user/Rvigoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure Groq and OpenRouter model access and generate bilingual Arabic or English speech through Groq-backed TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TTS input text is sent to Groq for speech generation. <br>
Mitigation: Avoid sending sensitive text unless Groq processing is acceptable for the deployment. <br>
Risk: The setup script installs Python packages from pip. <br>
Mitigation: Review requirements and install in a virtual environment before use. <br>
Risk: Speech generation may overwrite an existing canvas/speech.wav file. <br>
Mitigation: Run in a controlled workspace or preserve any existing audio file before generating new speech. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Rvigoo/openclaw-turbo-bundle5) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Model configuration example](artifact/config/MODELS_JSON_EXAMPLE.txt) <br>
- [Groq OpenAI-compatible API endpoint](https://api.groq.com/openai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, audio] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and WAV audio output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROQ_API_KEY and optionally OPENROUTER_API_KEY; speech generation writes canvas/speech.wav.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
