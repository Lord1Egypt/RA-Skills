## Description:

Creates Nano Banana 2 seeding images with realistic use contexts, observable product details, and space for advertising disclosure while avoiding unsupported claims or synthetic content presented as real consumer experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and commerce teams use this skill to draft prompts and shell commands for Nano Banana 2 product seeding images across social and e-commerce channels. It emphasizes authorized source material, visible disclosure areas, and observable claims for lifestyle, beauty, food, fashion, and product-experience imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key for image generation.

Mitigation: Use an environment variable or the skill's protected local config flow, keep the key private, and rotate it if it is exposed.

Risk: Reference images selected by the user may be uploaded to AI Hive or its upload storage.

Mitigation: Upload only authorized, non-sensitive images and avoid private, unlicensed, or identity-sensitive material.

Risk: Generated product seeding images can be misleading if synthetic content, sponsorship, or product claims are not disclosed.

Mitigation: Keep disclosure space in the image, label AI-generated content where required, and restrict claims to observable product details supported by the source material.

Risk: The helper depends on the Python requests package and network access to AI Hive.

Mitigation: Install dependencies in a virtual environment and review network access expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-seeding-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates or edits images through AI Hive, can upload user-selected reference images, polls task status, and downloads completed image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
