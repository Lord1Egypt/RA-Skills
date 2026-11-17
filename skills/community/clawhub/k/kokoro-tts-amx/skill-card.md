## Description:

Kokoro Tts Amx provides local Kokoro-82M text-to-speech on Intel CPUs, using PyTorch bf16 autocast and oneDNN AMX-BF16 acceleration to synthesize multilingual 24 kHz mono WAV audio without a cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wray151](https://clawhub.ai/user/wray151)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install and run offline Kokoro-82M speech synthesis for narration, dubbing, and multilingual text-to-speech workflows on local Intel CPU hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer performs shell setup steps, may invoke a system package manager with sudo, downloads Python and model dependencies, and can replace an existing kokoro-tts-amx skill directory.

Mitigation: Review install.sh before running it, prefer a locally cloned reviewed revision instead of the curl-to-bash one-liner, watch for the sudo prompt, and back up or inspect any existing kokoro-tts-amx skill directory first.

Risk: First use downloads model assets and dependencies, which may be unsuitable for offline or tightly controlled environments.

Mitigation: Pre-download and review required assets in a controlled environment, then copy the approved Hugging Face cache and virtual environment setup into the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wray151/skills/kokoro-tts-amx)
- [Kokoro-82M voice list](https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown with inline shell commands and generated 24 kHz mono WAV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally after setup; first use may download Kokoro-82M model assets and Python dependencies.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
