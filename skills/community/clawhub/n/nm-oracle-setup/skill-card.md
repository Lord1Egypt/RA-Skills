## Description:

Provisions the oracle ML inference daemon with onnxruntime via uv

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to provision the local Oracle ML inference environment for skill quality evaluation, including its Python environment and ONNX Runtime dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local reference could not be matched to a bundled artifact, so the security analysis is incomplete.

Mitigation: Review whether the unresolved reference matters to your installation before installing.

## Reference(s):

- [Project homepage (declared in skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/oracle)

## Skill Output:

**Output Type(s):** [Shell commands, Setup guidance, Text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the provisioning result and the model-directory prerequisite for daemon startup.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
