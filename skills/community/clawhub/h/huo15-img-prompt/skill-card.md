## Description: <br>
Huo15 Img Prompt helps agents create and refine text-to-image and text-to-video prompts, storyboard packages, brand kits, style presets, character cards, and review workflows for tools such as Midjourney, SDXL, Flux, and DALL-E 3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creative teams, and agent users use this skill to turn briefs, scripts, brand requirements, or reference images into reusable image and video generation prompts, prompt variants, storyboard assets, and local creative workflow files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, or reference material may be sent to external providers when optional API-backed features are used. <br>
Mitigation: Use provider-backed features only with approved content and accounts, and avoid submitting sensitive prompts or images unless the destination provider is trusted. <br>
Risk: The skill reads API keys from the environment and can use a custom Anthropic base URL. <br>
Mitigation: Provide only scoped credentials, keep them out of shared logs or prompts, and set ANTHROPIC_BASE_URL only to trusted endpoints. <br>
Risk: Creative material can be persisted locally in ~/.huo15 or exported to Obsidian paths. <br>
Mitigation: Review, secure, or delete local persisted assets and Obsidian exports when prompts, references, or generated assets are sensitive. <br>
Risk: The Web UI creates a local interaction surface. <br>
Mitigation: Run the Web UI on localhost only and avoid exposing it to untrusted networks. <br>
Risk: Prompt safety linting or polishing could be misused to bypass provider rules. <br>
Mitigation: Use safety and polish features to comply with provider policies, and review generated prompts before submission. <br>


## Reference(s): <br>
- [Huo15 Img Prompt ClawHub page](https://clawhub.ai/zhaobod1/huo15-img-prompt) <br>
- [Quickstart](QUICKSTART.md) <br>
- [Recipes](RECIPES.md) <br>
- [T2I prompt engineering reference](references/t2i-guide.md) <br>
- [Examples](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plain text prompts, shell commands, and local workflow files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate provider-specific prompt text, storyboard JSON, scene and transition prompt files, brand kit or character configuration, and review guidance.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
