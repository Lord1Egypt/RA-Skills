## Description:

Text-to-speech conversion using OpenAI's TTS API for generating high-quality, natural-sounding audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merend](https://clawhub.ai/user/merend)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to convert text, files, or piped input into speech audio for accessibility, narration, podcast-style output, or multitasking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text sent for conversion is processed by OpenAI's remote API and may include sensitive or regulated content.

Mitigation: Avoid using the skill on secrets, credentials, regulated data, or confidential documents unless remote processing is approved.

Risk: Broad activation wording could trigger remote text-to-speech conversion or audio file creation unexpectedly.

Mitigation: Review prompts and requested outputs before execution, especially when user text may contain sensitive material.

Risk: API usage may incur OpenAI costs and depends on local Python, package, and ffmpeg setup.

Mitigation: Confirm API budget and run the skill in an isolated virtual environment with pinned dependency versions.

## Reference(s):

- [OpenAI Text-to-Speech Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI Create Speech API Reference](https://platform.openai.com/docs/api-reference/audio/createSpeech)
- [OpenAI Pricing](https://openai.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated runtime artifacts are audio files such as mp3, opus, aac, or flac.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY; supports voice, model, output format, speed, file input, stdin, and long-text chunking.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
