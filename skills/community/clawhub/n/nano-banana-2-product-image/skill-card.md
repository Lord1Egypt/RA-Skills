## Description:

使用 Nano Banana 2 制作可用于提案、上新和营销测试的产品图，把商品事实、外观锚点、镜头、布光、材质和渠道比例组织成可验收的商业画面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Product marketers, ecommerce operators, designers, and agents use this skill to turn product facts, authorized reference images, and channel requirements into Nano Banana 2 product-image prompts and generation commands. It supports packshots, concept still life, color variants, functional relationship images, and seasonal hero shots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AI Hive API key and sends generation requests to an external service.

Mitigation: Use an isolated Python environment, keep the API key in an environment variable or 0600 config file, and review where generated images are saved.

Risk: Reference images may contain brand, product, or confidential visual material.

Mitigation: Upload only product and brand assets the user is authorized to use.

Risk: Generated product imagery can misrepresent product geometry, packaging, included accessories, or claims.

Mitigation: Check outputs against the product fact table and clearly label concept images, synthetic environments, and non-standard props.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/nano-banana-2-product-image)
- [AI Hive API Endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API Key Help](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authorized reference images when provided; generated files are saved to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
