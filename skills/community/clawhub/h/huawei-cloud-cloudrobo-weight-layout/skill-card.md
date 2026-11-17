## Description:

Standard directory layout and naming conventions for saving model weights (checkpoints).

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and machine learning engineers use this skill to organize final model weights and periodic checkpoints, update training save paths, and locate the latest checkpoint for resume or loading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loading untrusted .pt checkpoints may execute code; weights_only=True is not a guarantee that arbitrary model files are safe.

Mitigation: Load checkpoints only from trusted sources, prefer safetensors, and keep dependencies maintained with relevant security fixes.

## Reference(s):

- [Reference loader](references/loader.py)
- [Verification method](references/verification-method.md)
- [IAM policies](references/iam-policies.md)
- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-weight-layout)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with Python reference code and directory layout examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Framework-agnostic outer directory layout; checkpoint-internal files remain model-specific.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
