## Description:

This skill helps agents turn text-only creative briefs into executable GPT Image 2 prompts and submit image generation tasks through AI Hive without using reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create editorial header images, product concept visuals, illustrations, social media covers, poster backgrounds, and advertising concepts from text-only briefs. It guides prompt structure, acceptance criteria, batch and aspect-ratio settings, task lookup, and local downloads through AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unsafe API response could cause downloaded result files to be written outside the chosen output folder.

Mitigation: Use an output directory where unintended writes have limited impact and avoid running the tool with elevated privileges until filename containment is fixed.

Risk: The skill stores and uses an AI Hive API key locally.

Mitigation: Use it only on trusted machines, keep the local config file private, and prefer a virtual environment with least-privilege execution.

Risk: The skill sends prompts and authenticated generation requests to AI Hive.

Mitigation: Install only if you trust AI Hive with submitted prompts and API-key-backed image generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-text-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON task status, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed GPT Image 2 text-to-image model, accepts text prompts plus batch/aspect-ratio/routing settings, stores API keys locally with 0600 permissions, and saves generated image results to a local output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
