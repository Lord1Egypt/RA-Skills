## Description:

使用 GPT Image 2 制作基于真实商品事实和使用过程的种草图片，包括开箱、使用步骤、细节证据、生活场景、图文卡片和社媒封面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, and content teams use this skill to plan and generate product seeding visuals for e-commerce and social platforms. It helps structure evidence-led prompts for unboxing, usage steps, detail cards, lifestyle scenes, covers, and carousel images while avoiding unsupported product claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media files are sent to the configured AI Hive service.

Mitigation: Use the default HTTPS endpoint or another trusted endpoint, and avoid submitting confidential, regulated, or unapproved media.

Risk: The packaged script handles credentials, network requests, and local file downloads.

Mitigation: Run without elevated privileges, protect the API key, use a controlled output directory, and review downloaded results before reuse.

Risk: Product seeding images can imply unsupported claims, sponsorship, affiliate relationships, or user experience.

Mitigation: Use documented product facts, preserve disclosure text and approvals, and require qualified review for medical, beauty efficacy, food nutrition, children's, and financial products.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/gpt-image-2-seeding-image)
- [AI Hive API Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash command examples; CLI execution returns JSON task data and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompts and optional reference media; generated results are downloaded to a local output directory unless downloads are disabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
