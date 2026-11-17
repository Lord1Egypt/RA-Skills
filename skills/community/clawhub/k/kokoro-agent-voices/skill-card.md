## Description:

Kokoro Agent Voices provides local Kokoro TTS text-to-speech for agents with named voice profiles, 54 available voices, and WAV output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate local speech from agent text, assign voice profiles, list available voices, and save WAV audio without per-call TTS API costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional playback can execute unintended shell commands through the output filename.

Mitigation: Avoid --play and do not pass untrusted output paths until playback uses a non-shell subprocess call or equivalent safe audio playback.

Risk: First run downloads Kokoro model weights from Hugging Face Hub without server evidence of a pinned revision.

Mitigation: Confirm the model download fits the deployment supply-chain policy and pin or verify model artifacts where required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/kokoro-agent-voices)
- [Kokoro model on Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and WAV file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated speech is saved as WAV audio; first use may download Kokoro model weights from Hugging Face Hub, with later inference running locally.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
