## Description:

This skill uses GPT Image 2 through AI Hive to replace backgrounds for product and person images while preserving subject identity, edges, perspective, lighting, shadows, reflections, and transparent details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce teams, and developers use this skill to generate product and portrait background replacements for white-background images, commercial lifestyle scenes, campaign variants, identity-preserving people composites, and localized market environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI Hive API key through CLI arguments, environment variables, or a local config file.

Mitigation: Keep the key private, prefer environment or config storage with restricted permissions, and rotate the key if it is exposed.

Risk: The skill can use a custom AI_HIVE_BASE_URL or --base-url value.

Mitigation: Use the default AI Hive endpoint unless the replacement endpoint is fully trusted.

Risk: The upload command and generation workflow send local image files and prompts to the configured service.

Mitigation: Upload only files intended for the image task and avoid unrelated, confidential, or unapproved local files.

Risk: Background replacement can create misleading product or identity imagery.

Mitigation: Preserve the original image and disclose synthetic edits for high-risk product, evidence, or identity-sensitive use cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-background-replace)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and a Python CLI that submits image generation tasks, uploads reference images, polls task status, and downloads result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files are downloaded locally unless the user chooses submit-only mode.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
