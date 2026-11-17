## Description:

Hugging Face CLI to estimate the required memory to load Safetensors or GGUF model weights for inference from the Hugging Face Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to estimate whether Hugging Face Hub models with Safetensors or GGUF weights will fit available GPU or system memory before inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned external CLI package can introduce supply-chain risk.

Mitigation: Use a pinned, reviewed hf-mem version before installing or running the CLI.

Risk: Gated or private repositories may require a Hugging Face token with broader access than the task needs.

Mitigation: Use a least-privilege Hugging Face token and expose it only for the command that needs it.

Risk: GGUF repositories may contain several precision or quantization files, so estimating all files can overstate the memory needed for one inference run.

Mitigation: Specify --gguf-file for the exact file or path intended for inference.

## Reference(s):

- [ClawHub hf-mem release](https://clawhub.ai/huggingface/skills/hf-mem)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash commands and JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require HF_TOKEN or --hf-token for gated or private repositories; optional KV cache settings affect experimental estimates.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
