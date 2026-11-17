## Description:

Creates single-variable GPT Image 2 advertising test cells that lock product facts, audience, placement, landing-page claims, and invariants so performance marketers can compare attributable image variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Performance marketers and ecommerce teams use this skill to define control and variant ad-image cells for platforms such as Meta Ads, Google Display, Qianchuan, Xiaohongshu Ads, Amazon Ads, and TikTok Ads. It helps them generate or preview tightly constrained prompts where only one creative variable changes at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or unauthorized product images may be uploaded to an external image-generation service.

Mitigation: Use only images approved for submission to AI Hive and review confidentiality requirements before running the helper script.

Risk: The helper script performs broader upload and download network transfers than the documentation summarizes.

Mitigation: Review allowed hosts and file-transfer behavior before installation, prefer a virtual environment with pinned dependencies, and limit output downloads when needed.

Risk: Generated advertising images or prompts may imply unsupported product claims, offers, reviews, certifications, or performance results.

Mitigation: Keep claim and offer sources explicit, preserve the rejection constraints, and have humans review each creative against current advertising platform policies before launch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/image-2-ad-image)
- [AI Hive API](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples, generated prompt text, task status JSON, and downloaded image files from completed runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script fixes image generation to batchSize=1 for each cell and requires explicit product sources, product roles, five or more invariants, platform safe zones, landing-page messaging, and rejection constraints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
