## Description:

Create basic Transformers model adapters for msModelSlim and verify them through a four-step quantization workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers adapting decoder-only LLMs or understanding VLM text backbones use this skill to implement msModelSlim adapters and validate quantization workflows for supported models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification can execute model-supplied custom code without an explicit safety choice.

Mitigation: Review model code at a fixed revision, opt in before enabling custom-code execution, and run it in an isolated environment without credentials.

Risk: The workflow instructs users to run an external install.sh script.

Mitigation: Inspect install.sh before executing it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-msmodelslim-model-adapt)
- [Implementation Guide](artifact/references/implementation_guide.md)
- [Verification Guide](artifact/references/verification_guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Python adapter code, configuration examples, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapter and verification guidance for supported Transformers LLMs and VLM text backbones.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
