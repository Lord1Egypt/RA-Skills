## Description:

Helps agents use Nano Banana Pro through AI Hive for ecommerce product image cleanup, background replacement, white-background listings, realistic shadows, lifestyle scenes, and batch SKU image consistency as an alternative workflow for PhotoRoom-style tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, ecommerce operators, and agent users use this skill to generate shell commands and prompts for product image editing workflows, including white-background marketplace images, transparent-object edge handling, natural shadows, lifestyle background replacement, and consistent batch SKU outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images and prompts are sent to AI Hive for generation or editing.

Mitigation: Use only images and prompts suitable for AI Hive processing, and avoid submitting confidential or restricted product material unless authorized.

Risk: An AI Hive API key is required and may be supplied by command line, environment variable, or local config file.

Mitigation: Prefer the local config file or AI_HIVE_API_KEY environment variable over command-line secrets, and keep the config file permissions restricted.

Risk: Generated ecommerce images may alter product structure, colors, logos, shadows, or included accessories.

Mitigation: Run the documented edge and authenticity QA before publication, comparing output against the source product photos and current marketplace requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/photoroom-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload selected reference images and prompts to AI Hive, then poll tasks and download generated image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
