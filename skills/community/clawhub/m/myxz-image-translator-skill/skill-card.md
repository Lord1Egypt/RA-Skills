## Description:

妙言小智 (PicTech.cc) 专业级跨境电商图片翻译 Skill，支持批量翻译、主图保护、多语言映射、在线编辑与自动化工作流集成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pictechai](https://clawhub.ai/user/pictechai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and agent users use this skill to translate text in ecommerce product images from local files, folders, or image URLs while preserving layout and optionally protecting main product visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to PicTech/stableai.com.cn for translation.

Mitigation: Install only when this data transfer is acceptable for the images being processed.

Risk: VK API keys could be exposed if pasted into chat or logs.

Mitigation: Store the VK key in plugin configuration and do not include it in prompts, filenames, logs, or summaries.

Risk: The skill can fetch arbitrary image URLs without enough safeguards.

Mitigation: Avoid untrusted image URLs until URL allowlisting, private-network blocking, redirect validation, image/type checks, and download size limits are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pictechai/skills/myxz-image-translator-skill)
- [PicTech Official Website](https://www.pictech.cc)
- [PicTech Skill VK Setup](https://www.pictech.cc/newpictech/skills/openclaw-image-translation-skill)
- [PicTech API Service Domain](https://stableai.com.cn)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Structured JSON-style task result with translated image file paths, preview and editor URLs, counts, errors, and skipped items.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save translated image files locally and return remote result/editor URLs; caches repeated translations and marks no-text images as skipped.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
