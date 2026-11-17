## Description:

Uses Nano Banana 2 through AI Hive to edit existing images for cleanup, object replacement, color changes, layout adaptation, local subject/product adjustments, and batch variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to prepare image-editing prompts, run AI Hive image generation commands, and review differences against the original image for unintended changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys can be sent to a user-configurable AI Hive endpoint.

Mitigation: Keep the default base URL unless the endpoint is trusted, avoid untrusted AI_HIVE_BASE_URL or --base-url values, and use a limited API key where available.

Risk: The helper script contains broader AI Hive API capabilities than the advertised image-editing workflow.

Mitigation: Review the command being run and grant credentials only for the intended image-editing task.

Risk: Source images and generated outputs may contain sensitive content.

Mitigation: Review images before upload and confirm the download directory before running on sensitive material.

Risk: Runtime dependency installation can affect the local Python environment.

Mitigation: Install requests in a virtual environment before executing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-image-edit)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompts, source image paths, optional reference images, batch size, routing mode, API key, and base URL configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
