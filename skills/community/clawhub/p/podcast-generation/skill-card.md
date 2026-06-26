## Description: <br>
Generate AI-powered podcast-style audio narratives using Azure OpenAI's GPT Realtime Mini model via WebSocket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build text-to-speech and podcast-style audio generation workflows with Azure OpenAI Realtime API. It provides implementation guidance for environment setup, WebSocket streaming, audio event handling, PCM-to-WAV conversion, and frontend playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, bookmark summaries, or scripts are sent to Azure for audio generation. <br>
Mitigation: Use the skill only for content that is approved for Azure processing, and disclose this third-party processing to users of the resulting workflow. <br>
Risk: Generated audio and transcripts may contain user content and can become persistent records if stored. <br>
Mitigation: Define access controls, retention periods, and deletion paths before implementing the database-backed examples. <br>
Risk: Incorrect Realtime API configuration can cause failed audio generation or incomplete error handling. <br>
Mitigation: Use a WebSocket endpoint derived from the Azure base endpoint, configure audio output modalities, and handle Realtime API error events as shown in the acceptance criteria. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thegovind/podcast-generation) <br>
- [Architecture Reference](references/architecture.md) <br>
- [Code Examples](references/code-examples.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [PCM to WAV Conversion Script](scripts/pcm_to_wav.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Python, JavaScript, environment variable, and audio conversion examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
