## Description: <br>
Generates and edits images through LinkFox's multimodal image API using text prompts, optional reference image URLs, and aspect ratio settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate product images, edit photos, replace backgrounds, transfer styles, composite products into scenes, and swap models through LinkFox APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and reference image URLs are shared with LinkFox's image-generation API. <br>
Mitigation: Do not submit confidential prompts or private image URLs, and confirm that user-provided content may be sent to LinkFox before making API calls. <br>
Risk: The skill directs agents to send feedback details to a separate LinkFox endpoint, which may include user statements, secrets, or personal data. <br>
Mitigation: Disable automatic feedback submission or require explicit user review before sending feedback content. <br>
Risk: Reference images must be publicly accessible, which can fail for private URLs or expose sensitive images if access is broadened. <br>
Mitigation: Use only non-sensitive public reference URLs and remove or expire access after generation when possible. <br>


## Reference(s): <br>
- [AI drawing API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-multimodal-generate-image) <br>
- [LinkFox image generation endpoint](https://tool-gateway.linkfox.com/multimodal/generateImage) <br>
- [LinkFox feedback endpoint](https://skill-api.linkfox.com/api/v1/public/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Python script invocation and JSON API responses containing generated image markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; prompts and reference image URLs are sent to LinkFox APIs; supports up to 3 reference images and 1000-character prompt and reference URL limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
