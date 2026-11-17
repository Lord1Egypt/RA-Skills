## Description:

微信公众号/朋友圈营销内容智能体。输入产品/服务主题、卖点、讲师信息、配图需求，输出专业文案+结构化配图。触发词：发朋友圈、生成朋友圈文案、微信图文、朋友圈营销、create wechat post、generate wechat image post。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, small business owners, and content creators use this skill to produce Chinese WeChat Moments campaign copy, image prompts, generated poster assets, and final handoff markdown for products, services, courses, or promotions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The callback workflow is unauthenticated and can store arbitrary callback data.

Mitigation: Run the callback service only in a controlled local or authenticated environment, avoid public exposure, and add authentication and request size limits before using it beyond a trusted setup.

Risk: Campaign prompts, product details, QR images, contact details, and generated assets may be sent to external image generation services.

Mitigation: Use only non-sensitive campaign content unless the user accepts sending that data to the configured KIE or Seedream service.

Risk: QR/contact features can place private personal data directly into generated marketing assets.

Mitigation: Confirm that QR codes, names, and phone numbers are intended for publication before including them in the generated poster or final markdown.

Risk: Downloaded image results may be unsafe or unsuitable if returned through an exposed callback and download flow.

Mitigation: Review downloaded files before use and restrict the callback and download workflow to trusted task IDs and expected output locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffli2002/skills/jeff-wechat-post)
- [QR Code Configuration](references/config/qrcode-schema.md)
- [Copy Template](references/workflow/copy-template.md)
- [Image Layout - WeChat Moments Poster](references/workflow/image-layout.md)
- [dark-warm palette](references/palettes/dark-warm.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, image-generation prompts, PNG image files, QR configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes campaign assets under wechat-post/{topic-slug}/ and may call external image generation services when configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
