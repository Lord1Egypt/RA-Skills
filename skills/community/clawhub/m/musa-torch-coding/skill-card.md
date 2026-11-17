## Description:

Guides developers in generating and converting PyTorch code for Moore Threads MUSA GPUs using torch_musa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lipeidcc](https://clawhub.ai/user/lipeidcc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write PyTorch code for Moore Threads MUSA GPUs, convert CUDA-oriented PyTorch patterns to MUSA equivalents, and follow MUSA environment and distributed-training conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published metadata describes OpenAI Whisper transcription and requests OPENAI_API_KEY even though the artifact is for MUSA/PyTorch coding.

Mitigation: Treat the release as a MUSA/PyTorch coding skill only after the publisher corrects the metadata and removes the unrelated OpenAI API key requirement.

Risk: The CUDA-to-MUSA converter can rewrite Python files or entire directories when run without dry-run mode.

Mitigation: Run the converter in dry-run mode first, write converted output to a separate path, and review diffs before adopting generated files.

Risk: Some setup and troubleshooting guidance involves preconfigured GPU environments, native libraries, build commands, and privileged group changes.

Mitigation: Use an approved MUSA environment and require administrator review before changing system groups, driver paths, or build/install steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lipeidcc/skills/musa-torch-coding)
- [MUSA API reference](references/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell code examples; bundled scripts can generate converted Python files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a CUDA-to-MUSA conversion script and a YOLOv8n MUSA template.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
