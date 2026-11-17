## Description:

用 AI Hive Nano Banana 2 为真实商品逐张制作电商详情页、PDP、Amazon A+ 与 Listing 卖点图；每张图只表达一个已核准主张，并记录商品事实、主张来源、视觉证据、文案安全区和不可虚构项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, brand teams, designers, and developers use this skill to prepare fact-controlled product detail panels, PDP modules, Amazon A+ content, listing images, feature panels, material close-ups, how-it-works visuals, verified specifications, and comparison graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images are uploaded to AI Hive during panel generation.

Mitigation: Use only approved reference images that the user is allowed to upload, and run `preview` first when checking prompts without uploading assets.

Risk: Generated panels or required text could overstate product claims if not checked against source materials.

Mitigation: Keep each panel to one approved claim, provide claim sources and evidence for technical panels, and manually review any requested text before delivery.

Risk: Generated output files may be saved to the default downloads directory.

Mitigation: Use `--no-download` or set `--output-dir` when the user needs tighter control over saved files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/nano-banana-product-detail-page)
- [AI Hive API](https://ai-hive.iclip.cn/api)
- [AI Hive OpenAPI Endpoint](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, prompt previews, task status JSON, and generated PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Panel generation requires approved product reference images, an AI Hive API key, and manual review of any requested text before delivery.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
