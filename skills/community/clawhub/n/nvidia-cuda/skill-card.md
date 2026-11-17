## Description:

Use when work targets NVIDIA GPUs for deep learning training, inference, distributed execution, CUDA/Triton kernels, or AI infra tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkellyoffical](https://clawhub.ai/user/kkellyoffical)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to optimize and review CUDA/PyTorch training, inference, distributed execution, and GPU infrastructure decisions on NVIDIA hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CUDA and PyTorch probes can reveal hardware, driver, environment variable, and topology details.

Mitigation: Run probes only in trusted workspaces and redact system details before sharing outputs.

Risk: Benchmarks and smoke tests execute CUDA, NCCL, and PyTorch workloads that can consume GPU resources or fail on hosts without the expected runtime.

Mitigation: Confirm CUDA visibility, PyTorch compatibility, and distributed environment variables before running the bundled benchmark or smoke-test commands.

Risk: Optional install or publication commands that use latest package versions can reduce reproducibility.

Mitigation: Use an isolated environment and pinned package or CLI versions for reviewed releases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kkellyoffical/skills/nvidia-cuda)
- [README](README.md)
- [NVIDIA CUDA Skill Notes](references/official-notes.md)
- [Latest NVIDIA GPU Recommendations for AI Infra](references/latest-gpu-recommendations-2026-04.md)
- [Runtime Support](references/runtime-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands, code snippets, configuration examples, and optional JSON tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local CUDA/PyTorch probe results, heuristic scan findings, and benchmark summaries when the bundled scripts are used.]

## Skill Version(s):

0.4.0 (source: server release metadata and changelog, released 2026-04-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
