## Description:

Guides an end-to-end CloudRobo model adaptation workflow across Ascend NPU migration, checkpoint layout, training metrics, and protocol-based inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use it to adapt PyTorch VLA or robot foundation models for CloudRobo and Ascend, covering two or more stages such as NPU migration, checkpoint layout, training metrics, and inference protocol integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-supplied code changes may be trusted automatically.

Mitigation: Review proposed changes and require explicit approval before executing model-supplied code.

Risk: The test client may expose images outside the selected folder, and TLS verification needs to be restored.

Mitigation: Constrain image paths to the selected folder and restore TLS verification; until corrected, use synthetic images with a trusted loopback server.

Risk: Training runs in the background by default.

Mitigation: Use foreground mode or track the recorded process ID to control the training process.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Verification Method](references/verification-method.md)
- [IAM Policies and Access Control](references/iam-policies.md)
- [Ascend PyTorch Installation Guide](https://www.hiascend.com/document/detail/zh/Pytorch/latest/installguide/swinstall/docs/zh/installation_guide/installation_description.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Python and shell files, configuration guidance, and a Markdown workflow summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stage-gated workflow using the model project, dataset, Ascend environment, target inference protocol, and output path.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
