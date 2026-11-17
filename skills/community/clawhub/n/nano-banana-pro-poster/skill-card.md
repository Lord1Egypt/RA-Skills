## Description:

使用 Nano Banana Pro 以视觉隐喻、色彩、构图和材质建立有辨识度的海报艺术方向，并扩展同系列多尺寸版本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and agents use this skill to generate or edit poster concepts with Nano Banana Pro through AI Hive. It helps define visual propositions, metaphors, composition, material language, series rules, and acceptance checks for campaign, fashion, sports, retail, exhibition, and social poster work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real AI Hive API key may be stored locally and used by the script.

Mitigation: Use an isolated environment, protect the local config file, and rotate the API key if it may have been exposed.

Risk: Changing AI_HIVE_BASE_URL or --base-url can send credentials and media to an arbitrary endpoint.

Mitigation: Use the default trusted AI Hive endpoint unless the alternate destination is fully trusted.

Risk: Reference images and other selected media may be uploaded to AI Hive or object storage.

Mitigation: Upload only media the user is authorized to process and keep source and rights records for artist, person, brand, or collaboration materials.

Risk: The bundled AI Hive client exposes broader capabilities than the poster-generation purpose requires.

Mitigation: Review commands before execution and limit use to the documented poster generation, task lookup, upload, and initialization flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-poster)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown instructions with bash commands; generated image files and JSON task responses from AI Hive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports prompts, reference images, batch generation, aspect ratios, additional model parameters, output directories, and optional no-download task submission.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
