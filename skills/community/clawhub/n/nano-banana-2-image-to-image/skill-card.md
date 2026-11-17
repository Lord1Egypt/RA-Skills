## Description:

Helps agents use Nano Banana 2 through AI Hive to redraw sketches, photos, product images, and existing designs into controlled image-to-image variations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to turn selected reference images into controlled redraws, colorways, scene changes, weather or time variants, and format adaptations through AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images and prompts are sent to AI Hive for generation.

Mitigation: Use the skill only with images and prompts that are appropriate to share with AI Hive.

Risk: API keys can be exposed if passed through shell history or process listings.

Mitigation: Prefer the 0600 local config file or a carefully managed environment variable over the --api-key command line option.

Risk: Unpinned Python dependencies can change behavior between installs.

Mitigation: Install dependencies in a virtual environment and pin versions for managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-image-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one user-selected reference image and an AI Hive API key.]

## Skill Version(s):

1.0.1 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
