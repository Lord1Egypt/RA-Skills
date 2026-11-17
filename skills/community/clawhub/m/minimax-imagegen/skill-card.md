## Description:

MiniMax Image Generator helps agents turn image requests into MiniMax image-01 prompts, call the image generation API, download the first returned PNG, and report the prompt and parameters for iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asimons81](https://clawhub.ai/user/asimons81)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate image assets such as illustrations, banners, icons, hero images, social media visuals, UI mockups, and portraits from natural-language requests. It is intended to support prompt construction, MiniMax image generation, local file output, and concise iteration notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts are sent to MiniMax for generation.

Mitigation: Avoid including confidential, regulated, or otherwise sensitive information in prompts unless MiniMax use is approved for that data.

Risk: The helper script can write generated files to caller-chosen output paths without containment or overwrite protection.

Mitigation: Use trusted output paths and keep outputs in the intended workspace image directory until path handling is tightened.

Risk: The security verdict is suspicious because the skill deserves review before installation.

Mitigation: Review the skill and its local script before deployment, and install only if the API use and file-writing behavior match the intended environment.

## Reference(s):

- [MiniMax Image Generation API endpoint](https://api.minimax.io/v1/image_generation)
- [ClawHub skill release page](https://clawhub.ai/asimons81/skills/minimax-imagegen)
- [Publisher profile](https://clawhub.ai/user/asimons81)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown status with prompt and parameter details, plus generated PNG image files and JSON output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and writes generated images to a local workspace image directory by default.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
