## Description:

Create audiobooks from web content or text files. Handles content fetching, text processing, and TTS conversion with automatic fallback between ElevenLabs, OpenAI TTS, and gTTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn articles, essays, or text files into audiobook audio by fetching source text, cleaning and chunking it, and selecting an available TTS provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can fetch arbitrary URLs and may retrieve private or unintended content.

Mitigation: Use only public, non-sensitive URLs unless explicit URL validation and access controls are added.

Risk: Fetched text can be sent to external TTS providers.

Mitigation: Obtain provider consent and avoid sending sensitive text unless the chosen TTS provider and data handling terms are approved.

Risk: The example writes temporary audio chunks and a concat list in shared temporary paths.

Mitigation: Use secure temporary files and clean them up after validating ownership and path scope.

Risk: The complete example writes output under /root.

Mitigation: Run examples as a non-root user and choose an explicit user-writable output path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/pg-essay-to-audiobook-audiobook)
- [ElevenLabs text-to-speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})
- [OpenAI speech API endpoint](https://api.openai.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward generating MP3 audiobook files through web fetching, text cleanup, chunking, external TTS APIs, gTTS fallback, and ffmpeg concatenation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
