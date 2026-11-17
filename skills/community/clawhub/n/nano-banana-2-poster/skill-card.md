## Description:

使用 Nano Banana 2 设计具有明确焦点、信息层级、文字安全区和渠道比例的海报底图或短标题海报，可从文字开始或使用授权参考图通过 AI Hive 生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and agents use this skill to create poster base images and short-title poster concepts with planned hierarchy, safe text areas, channel aspect ratios, and optional authorized reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader trusts API-controlled filenames and URLs, which could write files outside the intended output folder if a compromised API response is used.

Mitigation: Run the skill in a constrained environment, use a dedicated output directory, and add filename and path validation before routine use.

Risk: Selected reference images may be uploaded to or retrieved through unexpected hosts if the API response is compromised.

Mitigation: Use the skill only with a trusted AI Hive API path and avoid sensitive reference images.

Risk: The skill can store an AI Hive API key locally.

Mitigation: Use a dedicated API key, keep the local config permissions restricted, and review the environment before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-poster)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples, JSON task responses, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed Nano Banana 2 image model through AI Hive and may store an API key locally with 0600 permissions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
