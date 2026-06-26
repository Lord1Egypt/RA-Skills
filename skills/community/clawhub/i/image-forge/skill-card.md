## Description: <br>
Image Forge routes image generation and editing requests through use-case, style, and subject signals, selecting GPT Image 2 or Gemini/Nano Banana backends and returning generated image files with prompt guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyqthu](https://clawhub.ai/user/chenyqthu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill as a single OpenClaw image-generation entry point for posters, avatars, product images, social media visuals, UI mockups, comics, game assets, infographics, logo showcase images, style transfer, reference-image editing, and multi-reference composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled prompt libraries may enable identity-document, celebrity-likeness, profiling, sexualized, or externally researched image workflows. <br>
Mitigation: Review and prune the reference libraries before deployment, and enforce an image-use policy for disallowed or consent-sensitive requests. <br>
Risk: Prompts and reference images can be sent to the configured GPT Image 2 or Gemini/Nano Banana backend. <br>
Mitigation: Use only trusted endpoints and avoid private photos, government IDs, real-person likenesses, or private conversation context unless there is clear consent. <br>
Risk: The skill requires sensitive backend credentials for image generation services. <br>
Mitigation: Scope and protect API keys, keep credentials out of prompts and logs, and rotate keys if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenyqthu/image-forge) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Backend Registry](artifact/backends.yaml) <br>
- [Use-Case Index](artifact/use-cases/index.yaml) <br>
- [Style Index](artifact/styles/index.yaml) <br>
- [YouMind OpenLab awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) <br>
- [EvoLinkAI awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) <br>
- [YouMind OpenLab awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown responses with shell commands and MEDIA file paths; generated image files saved to disk.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured backend credentials and may send prompts or reference images to the selected image service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
