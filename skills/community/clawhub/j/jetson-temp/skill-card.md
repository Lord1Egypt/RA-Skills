## Description:

Monitors CPU, GPU, and thermal-zone temperatures on NVIDIA Jetson devices running Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxd9199](https://clawhub.ai/user/wxd9199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working with NVIDIA Jetson devices use this skill to check live local thermal readings while diagnosing device temperature or cooling behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Linux thermal subsystem files and is intended for NVIDIA Jetson hardware.

Mitigation: Run it on supported Jetson/Linux devices and treat missing or empty readings as an environment compatibility issue.

Risk: Thermal zone readings may not be self-describing on every device.

Mitigation: Confirm the target device's thermal zone mapping before using readings for operational or hardware decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxd9199/skills/jetson-temp)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and terminal output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Linux thermal sensor files and prints temperature values; security evidence reports no network access, credential use, persistence, or file modification.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
