## Description:

Helps agents translate LiblibAI, 哩布哩布 AI, Liblib, libtv, or model-community image workflows into observable Nano Banana Pro visual prompts without copying checkpoints, LoRAs, samplers, or seeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and image-production teams use this skill to migrate model-community image-generation recipes into rights-aware visual specifications and AI Hive image-generation commands. It is suited for prompt-based image generation and editing where source references must be authorized and third-party model weights are not redistributed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script trusts service-supplied upload and download details, which can send selected images to unexpected destinations or affect local files.

Mitigation: Use a dedicated AI Hive API key, avoid sensitive reference images, run in an isolated Python environment, and keep outputs in a non-sensitive directory.

Risk: Downloaded result files may be unsafe if redirects, hosts, sizes, or final paths are not constrained.

Mitigation: Validate storage and download domains, reject redirects to unexpected hosts, enforce download size limits, and ensure downloaded files cannot escape the chosen output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/liblibai-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and local CLI output; generated image files can be downloaded by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY or ~/.ai-hive/config.json, calls the fixed public_model_nano_banana_pro image model, and downloads successful task results to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
