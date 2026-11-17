## Description:

Provides system monitoring, performance analysis, and status information for NVIDIA Jetson devices, including GPU, CPU, memory, temperature, disk, and JetPack checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxd9199](https://clawhub.ai/user/wxd9199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working with NVIDIA Jetson devices use this skill to get local monitoring commands and checks for GPU, CPU, memory, disk, temperature, and JetPack status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Jetson-specific local utilities and may provide incomplete command coverage when tegrastats or jetson_release is unavailable.

Mitigation: Use it on Jetson systems with the required utilities installed, and verify each generated command before relying on the output.

Risk: Server quality evidence quarantined the release for moderation review due to low documentation quality.

Mitigation: Review the skill documentation and script behavior before deployment, especially where command names are documented but not implemented in the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxd9199/skills/jetson-tools)
- [Publisher profile](https://clawhub.ai/user/wxd9199)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and local system status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Jetson utilities such as tegrastats and jetson_release for full coverage.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
