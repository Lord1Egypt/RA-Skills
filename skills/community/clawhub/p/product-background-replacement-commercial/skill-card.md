## Description:

用 AI Hive Nano Banana Pro 将已授权商品图合成为白底、生活方式、节日、门店或广告场景，并尽量保持商品轮廓、结构、材质、Logo、比例、透视、光线和接触关系。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, photographers, and brand teams use this skill to create commercial product background replacements and marketplace scene images from authorized product images. It helps agents prepare prompts and commands for white-background, lifestyle, storefront, social ad, campaign, and localized seasonal composites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected product and background images to the AI Hive service.

Mitigation: Use only images the user is authorized to process, confirm trust in the AI Hive service, and avoid confidential or sensitive images unless that upload is approved.

Risk: The security summary reports that result downloading can write outside the chosen output folder or consume excessive disk space.

Mitigation: Run the skill in an isolated environment, use a dedicated output folder away from sensitive directories, and patch output containment and download size limits before production use.

Risk: The security guidance calls for task ID validation and pinned dependency fixes before production use.

Mitigation: Validate task identifiers, pin dependencies, and review the script before installing it into a shared or production agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-background-replacement-commercial)
- [AI Hive API endpoint used by the skill](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and user-provided authorized product or background images.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
