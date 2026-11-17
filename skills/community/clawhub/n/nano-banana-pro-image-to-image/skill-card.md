## Description:

Nano Banana Pro 图生图 helps agents transform reference images through AI Hive while preserving identity, product, space, composition, color, material, and lighting anchors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, designers, and agent operators use this skill to generate image-to-image prompts and commands for product visuals, portrait restyling, photo-to-illustration conversion, interior redesign, and multi-channel creative variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive reference images may be uploaded to a remote AI image service.

Mitigation: Use only images you are authorized to process, avoid sensitive inputs, and run the skill in an isolated Python environment when handling private work.

Risk: The bundled script stores and uses an AI Hive API key for authenticated requests.

Mitigation: Use a minimally scoped AI Hive key and rely on the local config path with file permissions restricted to 0600.

Risk: Remote task data can influence result download URLs and output filenames.

Mitigation: Choose a non-sensitive output directory and review downloaded files before using them in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-image-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline bash commands; script runs can emit JSON task data and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one reference image for generation and an AI_HIVE_API_KEY or local AI Hive config.]

## Skill Version(s):

1.0.1 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
