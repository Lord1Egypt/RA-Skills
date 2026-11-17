## Description:

Helps agents migrate Midjourney /imagine, style-reference, and image-prompt workflows to AI Hive Nano Banana Pro by turning proprietary prompt parameters into observable composition, style, reference-image, and commercial acceptance decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, and developers use this skill to translate Midjourney-style image generation or editing workflows into AI Hive Nano Banana Pro prompts, reference-image roles, candidate selection criteria, and CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images are sent to AI Hive.

Mitigation: Avoid confidential images, unreleased brand assets, or other sensitive prompts unless AI Hive's terms and the user's policy allow that processing.

Risk: A compromised API response could cause generated downloads to be saved outside the intended output folder.

Mitigation: Use a dedicated output directory and review downloaded paths; the publisher should sanitize output paths and restrict downloads to validated HTTPS media URLs before routine-risk use.

Risk: The tool depends on a local AI Hive API key.

Mitigation: Use a dedicated API key, prefer environment-based configuration or the generated config file with restricted permissions, and run the tool in a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/midjourney-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash command examples; CLI output includes task JSON and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive API key, optional reference images, batch size, routing mode, model parameters such as aspect_ratio, and a configurable output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
