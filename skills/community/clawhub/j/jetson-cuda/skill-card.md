## Description:

Provides NVIDIA Jetson CUDA tools to query CUDA version, GPU device information, and CUDA library paths on Jetson devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxd9199](https://clawhub.ai/user/wxd9199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working on NVIDIA Jetson devices use this skill to check local CUDA Toolkit availability, GPU status, and related CUDA environment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on local CUDA Toolkit and nvidia-smi availability, so results may be incomplete or report missing tools on systems without those dependencies.

Mitigation: Run it on the intended Jetson target and confirm CUDA Toolkit and nvidia-smi are installed before relying on the reported status.

Risk: Usage notes are Chinese-only in the inspected artifact, which can lead to misunderstanding during review or installation.

Mitigation: Have a reviewer who can read the usage notes confirm the commands and prerequisites before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxd9199/skills/jetson-cuda)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and local command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CUDA Toolkit and nvidia-smi on the target Jetson system for full results.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
