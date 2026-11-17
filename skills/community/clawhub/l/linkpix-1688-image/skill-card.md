## Description:

帮助 1688 批发商、源头工厂和 B2B 运营通过青虎 AI 生成商品主图套图、详情图和活动图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

1688 sellers, source factories, and B2B commerce operators use this skill to create product main-image sets, detail-page images, and promotional posters from product photos and brief copy.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Setup guidance asks users to share an API key in chat.

Mitigation: Keep the key in local configuration or an environment variable; do not send it in chat.

Risk: The workflow permits automatic installation and updating of external software whose dependencies were not inspected.

Mitigation: Review the package and dependency versions before installing or upgrading, and install only when trusted.

Risk: Product images are uploaded to Qinghu AI and generation consumes credits.

Mitigation: Use only product images approved for upload, and review the selected generation settings and estimate before submitting.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix ClawHub release page](https://clawhub.ai/autoagc/skills/linkpix-1688-image)

## Skill Output:

**Output Type(s):** [Images, Image generation guidance]

**Output Format:** [Generated product image files returned as image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Main-image sets, detail-page images, and promotional posters based on supplied product images and copy.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
