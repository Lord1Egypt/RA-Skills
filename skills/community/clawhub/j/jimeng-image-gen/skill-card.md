## Description: <br>
Generates images with Volcengine Jimeng AI Image Generation 4.0, supporting text-to-image, image-to-image, font design, poster-style prompts, and up to 4K output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken0521](https://clawhub.ai/user/ken0521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to request Jimeng image generation from an agent, including text prompts, reference-image edits, font design, poster concepts, resolution presets, and optional local image saving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to Volcengine for image generation. <br>
Mitigation: Avoid private, internal, or sensitive image URLs and prompts unless their disclosure to Volcengine is acceptable. <br>
Risk: Generation uses the user's Jimeng account quota and may incur costs based on output image count. <br>
Mitigation: Use a dedicated API key where possible and pass --force-single when cost control matters. <br>
Risk: Generated image URLs are temporary and may expire. <br>
Mitigation: Save needed outputs promptly after generation. <br>


## Reference(s): <br>
- [Jimeng AI Image Generation on ClawHub](https://clawhub.ai/ken0521/jimeng-image-gen) <br>
- [Publisher Profile](https://clawhub.ai/user/ken0521) <br>
- [Volcengine Jimeng Product Page](https://www.volcengine.com/product/jimeng) <br>
- [Jimeng API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated image file URLs or saved files from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus JIMENG_ACCESS_KEY and JIMENG_SECRET_KEY for Volcengine API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
