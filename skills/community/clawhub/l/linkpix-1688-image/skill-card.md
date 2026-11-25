## Description:

为1688批发商、源头工厂和B2B运营人员提供商品主图套图、详情图及活动图的生成工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

1688卖家、源头工厂和B2B运营人员可使用此技能，根据商品素材制作平台主图套图、详情图和促销活动图。

### Deployment Geography for Use:

China (1688 marketplace focus)

## Known Risks and Mitigations:

Risk: The package dependency may change after review because its version is not pinned in the installation guidance.

Mitigation: Review the package and selected version before installation; use a pinned version when the deployment supports it.

Risk: The workflow may request an API key in chat.

Mitigation: Configure the key through a secure local configuration or environment variable, and avoid sending the secret in chat.

Risk: Reference product images may be uploaded to an external service without a clear privacy warning.

Mitigation: Confirm the user is comfortable sharing each image with the service and remove confidential material before upload.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-1688-image)

## Skill Output:

**Output Type(s):** [Images, Text, Shell commands, Guidance]

**Output Format:** [Generated product images with Markdown guidance and inline shell or JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image requests can use product references, copy, platform settings, and available model choices.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
