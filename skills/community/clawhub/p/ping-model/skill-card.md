## Description:

Displays formatted ping and comparison output for current or named AI models, with latency values that the security evidence identifies as simulated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dofbi](https://clawhub.ai/user/dofbi)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to run a formatted ping command for the current or named model and compare displayed response timings across model names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present simulated latency numbers as real model measurements.

Mitigation: Treat the output as a formatting utility unless the implementation is changed to make real requests and clearly disclose the measurement method.

Risk: Users may rely on model rankings or timing output for operational decisions.

Mitigation: Do not use the displayed rankings or timing values for operational decisions without independent benchmarking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dofbi/skills/ping-model)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js. The security evidence states that the displayed timings are simulated and should not be treated as operational benchmarks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
