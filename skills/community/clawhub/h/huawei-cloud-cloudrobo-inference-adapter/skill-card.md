## Description:

Guides adapting a VLA model's inference server interface to the CloudRobo standard interface/protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers adapting vision-language-action model inference servers use this skill to map a model's inputs and outputs to the CloudRobo client protocol. It guides implementation and testing of the adapter, transport server, and client workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The test client may disclose images from outside the selected folder.

Mitigation: Constrain image paths to the selected directory and validate camera names before loading or sending images.

Risk: The inference server may be exposed to unauthorized access or resource-exhaustion requests.

Mitigation: Restrict server access and enforce finite message and array limits.

Risk: The client may send real images without verifying the server certificate, and server errors may expose details.

Mitigation: Verify the server certificate before sending real images and return sanitized errors.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-inference-adapter)
- [Publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [Adapter template](references/adapter_template.py)
- [Transport server template](references/server_template.py)
- [IAM and access policy guidance](references/iam-policies.md)
- [Adapter verification script](scripts/verify_adapter.py)
- [Inference test client](scripts/test_client.py)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapter conversion logic is model-specific and must follow the target model's interface and metadata.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
