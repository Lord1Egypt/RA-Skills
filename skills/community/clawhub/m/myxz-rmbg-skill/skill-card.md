## Description:

妙言小智 (PicTech.cc) 专业级跨境电商图片抠图/白底图工具。使用本 skill 处理图片去背景、透明底图、白底图、纯色背景图、本地图片、网络图片、文件夹图片和批量抠图任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pictechai](https://clawhub.ai/user/pictechai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to remove image backgrounds, create transparent PNGs, and generate white or solid-color product images for ecommerce listing workflows. It supports local image files, image folders, image URLs, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to PicTech/stableai for processing.

Mitigation: Avoid sensitive photos or private business images unless the user trusts the service and its handling of uploaded content.

Risk: The skill requires a VK API key.

Mitigation: Use a scoped configuration or environment secret, and do not paste API keys into chat or expose them in replies.

Risk: URL inputs may cause the skill to fetch arbitrary remote images.

Mitigation: Process only trusted URLs until URL validation and size limits are added.

Risk: The security summary flags dependency hygiene as review-worthy.

Mitigation: Review dependency versions and scanner results before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pictechai/skills/myxz-rmbg-skill)
- [PicTech.cc](https://www.pictech.cc)
- [PicTech VK key page](https://www.pictech.cc/newpictech/skills/openclaw-image-translation-skill)
- [StableAI image background removal service](https://stableai.com.cn/myxz/skill/imagermbg)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [JSON result object with saved PNG file paths, result URLs, counts, and failure details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are PNG images saved locally, with optional transparent, white, black, or custom solid-color backgrounds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
