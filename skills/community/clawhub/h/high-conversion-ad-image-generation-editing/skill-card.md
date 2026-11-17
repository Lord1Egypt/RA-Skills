## Description:

使用 Nano Banana Pro 生成和编辑广告图片，并通过漏斗诊断、信息匹配、单变量实验和真实结果复盘寻找更高转化候选；通过 AI Hive 生成，高转化不构成保证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, marketers, creative operators, and developers use this skill to generate and edit performance ad image candidates for channels such as Meta Ads, Google Ads, TikTok Ads, Amazon Ads, Douyin Qianchuan, and Xiaohongshu Juguang. It helps structure funnel diagnosis, landing-page matching, single-variable creative experiments, and post-test review, while treating higher conversion as a test hypothesis rather than a guaranteed outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports a real file-write safety issue when saving API-returned results.

Mitigation: Use a dedicated output directory, avoid elevated privileges, and review downloaded result paths before relying on generated files.

Risk: The security guidance warns that input images are uploaded to AI Hive.

Mitigation: Use only images that are approved for upload to AI Hive and avoid sensitive or unlicensed source material.

Risk: The security guidance recommends path containment, upload/download host validation, and download size limits before treating the skill as routine-risk.

Mitigation: Keep use isolated, prefer a virtual environment, and require publisher fixes for path containment, host validation, and download size limits before broad deployment.

Risk: The artifact states that generated ad creatives are test candidates and do not guarantee higher conversion.

Mitigation: Run controlled A/B tests, keep non-target variables stable, and decide retention or revision from real click, page behavior, and conversion data.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/high-conversion-ad-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with bash command examples, JSON task responses, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to a user-selected output directory or the default ~/Downloads/AiHive path; task polling can also return JSON without downloading files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
