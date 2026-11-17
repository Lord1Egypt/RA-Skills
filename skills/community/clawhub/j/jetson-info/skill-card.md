## Description:

Query NVIDIA Jetson device model, JetPack, L4T, CUDA/cuDNN/TensorRT versions, serial number, and hardware specs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxd9199](https://clawhub.ai/user/wxd9199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working with NVIDIA Jetson devices use this skill to inspect local hardware identity and installed Jetson software versions from command-line output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local command output may display device identifiers such as a serial number.

Mitigation: Use the skill only where showing local Jetson identifiers to the operator is acceptable, and avoid sharing captured output externally unless identifiers are removed.

Risk: The helper depends on jetson_release from jetson-stats and will provide limited value when that tool is not installed.

Mitigation: Install and verify jetson-stats on the target Jetson device before relying on the reported hardware and software version details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxd9199/skills/jetson-info)
- [Publisher profile](https://clawhub.ai/user/wxd9199)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and terminal-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May display local device identifiers such as a serial number when reported by jetson_release.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
