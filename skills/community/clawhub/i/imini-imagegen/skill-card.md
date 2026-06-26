## Description: <br>
Use this skill when the user wants to generate raster images through the imini image generation API, including text-to-image and image-guided generation with public image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horseson2018](https://clawhub.ai/user/horseson2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate raster images from text prompts or public reference image URLs through the imini image generation API, then save the resulting files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and public reference image URLs are sent to the imini image generation API. <br>
Mitigation: Install only if that data flow is acceptable, avoid sensitive prompts or private images, and use only public reference URLs intended for external processing. <br>
Risk: The skill depends on a local API key and configurable API base URL. <br>
Mitigation: Keep IMINI_IMAGE_API_KEY in the local environment or skill config, do not place keys in prompts or files, and verify the configured base URL before use. <br>
Risk: Generated files are written to the workspace. <br>
Mitigation: Review saved files under output/imagegen or the selected output directory before sharing or deploying them. <br>


## Reference(s): <br>
- [IMINI Nano Banana API Reference](references/api.md) <br>
- [IMINI ImageGen Configuration](references/config.md) <br>
- [IMINI Nano Banana Documentation](https://nexuslinelimited-1d434f54.mintlify.app/zh/api-reference/images/nano-banana) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local image files saved by the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and IMINI_IMAGE_API_KEY; generated image files are saved under output/imagegen unless another output directory is provided.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
