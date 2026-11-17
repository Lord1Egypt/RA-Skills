## Description:

根据一张服装模特图自动生成多种姿势及展示角度的套图，丰富商品展示效果，适用于服装详情页及社交媒体营销。当用户要求模特多姿势、多角度展示图、服装套图、一张模特图出一组时必须触发。关键词：LinkPix、qhkit、多姿势、姿势套图、多角度、模特套图、服装展示、详情页套图、社媒素材、pose。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce and marketing users provide a clothing model photo to create a coordinated set of pose and viewing angle variations for product pages or social media. The agent can also generate a single requested pose and guide the user to review important garment details in the results.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Source photos are uploaded to iqinghu.com, and image generation consumes account credits.

Mitigation: Only upload photos you are comfortable sharing with the service, and check the generation estimate before starting a job.

Risk: Qinghu credentials may be reused on an OpenClaw machine, while the external qhkit CLI can change across releases.

Mitigation: Protect the API key and use a reviewed CLI version; upgrade deliberately after reviewing the package guidance.

Risk: Generated variations may alter small model or garment details.

Mitigation: Review text, logos, and product structure before using generated images in product listings or marketing.

## Reference(s):

- [qhkit package documentation](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-model-pose-set)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated image files delivered as image URLs, with a concise Markdown response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated variations may have small differences in model or garment details; review text, logos, and product structure before publishing.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
