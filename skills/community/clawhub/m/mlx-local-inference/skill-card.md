## Description:

Use when calling local AI on an Apple Silicon Mac for text generation, embeddings, speech-to-text, OCR, or image understanding through a local oMLX gateway and MLX Python libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bendusy](https://clawhub.ai/user/bendusy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route local inference tasks on Apple Silicon Macs, including OpenAI-compatible local chat, embeddings, speech-to-text, OCR, and image understanding. It is suited for privacy-sensitive or low-latency workflows that avoid cloud AI APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users or agents to run local Python package commands and service-management commands on a Mac.

Mitigation: Review commands before execution, install uv through a verified channel, pin or lock MLX dependencies where possible, and require explicit confirmation before restarting services.

Risk: Local inference may process sensitive local files for OCR, ASR, embeddings, or image understanding.

Mitigation: Run inference with only the needed files accessible and avoid granting broad filesystem access to the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bendusy/skills/mlx-local-inference)
- [uv installer](https://astral.sh/uv/install.sh)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local inference setup and usage guidance for macOS; does not itself return model outputs.]

## Skill Version(s):

2.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
