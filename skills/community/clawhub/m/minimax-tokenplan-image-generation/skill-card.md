## Description: <br>
Generates images with the MiniMax image-01 model from text prompts or a single reference image, with prompt optimization and watermark controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4833675](https://clawhub.ai/user/4833675) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images through MiniMax image-01 from text prompts or a single reference image, then receive saved image files or short-lived image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup asks users to save a MiniMax API key in plaintext skill files. <br>
Mitigation: Use an environment variable or secret manager for MINIMAX_API_KEY, and do not store the key in SKILL.md or generate.py. <br>
Risk: Prompts and selected reference images are sent to MiniMax during generation. <br>
Mitigation: Only submit prompts and local image paths the user intentionally wants uploaded, and avoid sensitive or confidential content. <br>


## Reference(s): <br>
- [MiniMax Image Generation Documentation](https://platform.minimaxi.com/docs/guides/image-generation) <br>
- [ClawHub Skill Page](https://clawhub.ai/4833675/minimax-tokenplan-image-generation) <br>
- [ClawHub Install Listing](https://clawhub.ai/skills/minimax-tokenplan-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration] <br>
**Output Format:** [PNG image file paths or short-lived image URLs printed to stdout; stderr contains logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports up to 9 images per request; prompts are limited to 1500 characters; URL responses expire after 24 hours.] <br>

## Skill Version(s): <br>
0.9.5 (source: SKILL.md frontmatter and CHANGELOG, released 2026-04-05) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
