## Description:

Generates 3D models from text, images, multi-view images, sketches, or geometry and topology options using Tencent Cloud Hunyuan 3D 3.0 and 3.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to submit and monitor Tencent Cloud Hunyuan 3D generation jobs from text or image inputs, then return generated model file URLs and preview assets to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation prompts, images, and related job data are sent to Tencent Cloud.

Mitigation: Use the skill only when cloud processing is acceptable for the input data, and run it in an isolated environment with least-privilege Tencent credentials.

Risk: The scripts can install an unpinned Tencent SDK at runtime.

Mitigation: Preinstall a pinned, reviewed Tencent SDK version before use and review dependency changes during deployment.

Risk: Long-lived Tencent credentials may be exposed if stored in shell startup files on shared systems.

Mitigation: Prefer short-lived credentials and avoid placing persistent secrets in shared shell profiles.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/neck-cn/skills/hy-3d-generation)
- [Tencent Cloud 3D Vision Creation Console](https://console.cloud.tencent.com/ai3d)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON command output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns job IDs, status, generated model file URLs, and preview image URLs when Tencent Cloud generation completes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
