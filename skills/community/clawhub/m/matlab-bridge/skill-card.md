## Description:

Matlab Bridge lets an agent run MATLAB code and scripts for simulation, data analysis, signal processing, and plotting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and researchers use this skill to route MATLAB-based numerical computation, signal processing, plotting, and existing .m script execution through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute local MATLAB code and write files with broad access.

Mitigation: Run it in a low-privilege environment with a dedicated input/output directory and review code before execution.

Risk: Untrusted file names, labels, template parameters, or script arguments can affect MATLAB execution and generated files.

Mitigation: Avoid untrusted inputs, constrain paths to expected working directories, and validate script arguments before use.

Risk: Generated .mat, JSON, CSV, and plot outputs may contain sensitive workspace data.

Mitigation: Review generated outputs before sharing and disable workspace saving unless it is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/matlab-bridge)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with MATLAB, Python, and shell command snippets; execution results may include JSON, MAT, CSV, and plot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to a configured MATLAB output directory, and workspace data may be saved when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
