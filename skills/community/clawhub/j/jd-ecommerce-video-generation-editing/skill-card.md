## Description:

为京东商品页和京准通生成与编辑3C家电演示、参数结构、安装操作及广告视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and ecommerce operators use this skill to produce or edit JD product-page and advertising videos for 3C electronics, appliances, installation workflows, interface demonstrations, and approved product claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected product media may be sent to AI Hive during generation, editing, upload, and task polling workflows.

Mitigation: Use the skill only with media and prompts that are appropriate to share with AI Hive, and avoid including confidential product data unless approved.

Risk: API keys can be sent to a configured base URL, including custom CLI or AI_HIVE_BASE_URL endpoints.

Mitigation: Use the default official API URL unless a custom endpoint is fully trusted, and prefer a limited API key.

Risk: Generated outputs may be downloaded to a user-selected output directory.

Mitigation: Choose an output directory where accidental file writes will not damage important data, or use no-download mode when only task submission is needed.

Risk: Generated videos can contain inaccurate technical claims if prompts include unverified product details.

Mitigation: Build prompts from merchant-provided or visible evidence and manually review parameters, compatibility, certifications, warranty text, and performance claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/jd-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit API calls to AI Hive, upload selected media, poll task IDs, and download generated image or video files unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
