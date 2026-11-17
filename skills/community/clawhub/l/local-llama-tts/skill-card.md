## Description:

Local text-to-speech using llama-tts (llama.cpp) and OuteTTS-1.0-0.6B model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxxin](https://clawhub.ai/user/wuxxin)

### License/Terms of Use:


## Use Case:

Developers and audio-focused agents use this skill to synthesize WAV speech locally from text using llama-tts with OuteTTS and WavTokenizer model files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model and vocoder downloads may be unverified if users fetch them without pinned checksums.

Mitigation: Use trusted model sources and prefer pinned downloads with published SHA-256 checksums before local execution.

Risk: Untrusted speaker filenames may trigger unsafe shell argument handling in the wrapper script.

Mitigation: Use trusted local speaker files only, validate option values, and update the wrapper to pass arguments through an array.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuxxin/skills/local-llama-tts)
- [OuteAI OuteTTS-1.0-0.6B GGUF model](https://huggingface.co/OuteAI/OuteTTS-1.0-0.6B-GGUF/resolve/main/OuteTTS-1.0-0.6B-Q4_K_M.gguf?download=true)
- [ggml-org WavTokenizer model](https://huggingface.co/ggml-org/WavTokenizer/resolve/main/WavTokenizer-Large-75-Q5_1.gguf?download=true)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapper script writes a WAV file when executed with local model files.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
