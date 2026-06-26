## Description: <br>
Generate Gumroad product cover and preview images from local HTML templates, theme settings, and headless browser screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[careytian-ai](https://clawhub.ai/user/careytian-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and marketplace operators use this skill to generate Gumroad product covers, showcase images, and thumbnails from structured product information without external image-generation APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Serving a broad local directory could expose unrelated local files during image generation. <br>
Mitigation: Use a dedicated product-images folder for the local HTTP server and stop the server after screenshots are complete. <br>
Risk: An untrusted transient http-server install could introduce package supply-chain risk. <br>
Mitigation: Use a trusted or pinned http-server installation before running the screenshot workflow. <br>
Risk: Generated Gumroad images may become misleading if they include volatile pricing language. <br>
Mitigation: Follow the artifact guidance to avoid prices or free claims in generated images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/careytian-ai/gumroad-product-images) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML templates, JSON theme configuration, and PowerShell screenshot commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local HTML and PNG image-generation instructions for 600x600 cover images and 1280x720 preview images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
