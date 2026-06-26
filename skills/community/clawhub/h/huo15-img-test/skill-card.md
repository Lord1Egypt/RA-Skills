## Description: <br>
Huo15 Img Test helps agents turn image or video ideas into model-specific prompts, optional JSON recipes, prompt rewrites, reference-image prompt analysis, and image-generation commands for Midjourney, Stable Diffusion, SDXL, Flux, DALL-E, ComfyUI, and SD WebUI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to produce polished text-to-image and text-to-video prompts, keep visual series more consistent, reverse-engineer reference-image prompts, and prepare commands or JSON recipes for supported image generation backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The safety rewrite feature intentionally rewrites sensitive prompts to improve acceptance by image platforms, which could be misused to bypass platform rules. <br>
Mitigation: Review rewritten prompts manually, use the feature only for compliant artistic work, and do not treat the rewrite as a guarantee of platform or policy compliance. <br>
Risk: Optional cloud-backed polish and image generation can expose prompts or images to third-party services when API keys or endpoint URLs are configured. <br>
Mitigation: Set only the provider keys needed for the task, keep endpoint override variables pointed at trusted services, and avoid sending confidential prompts or images unless the relevant provider terms are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-img-test) <br>
- [Text-to-image guide](references/t2i-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable prompts and guidance, Markdown command examples, and optional JSON recipes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user-provided API keys for optional Claude or DALL-E features and may send prompts or images to configured cloud or local generation backends.] <br>

## Skill Version(s): <br>
2.3.0 (source: frontmatter, changelog, server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
