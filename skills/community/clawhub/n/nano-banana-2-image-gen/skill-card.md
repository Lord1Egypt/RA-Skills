## Description: <br>
Generates and edits images from text prompts or input images using the APIYI-hosted Gemini/NanoBanana2 image endpoint with configurable aspect ratio and resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent create new images or edit supplied images for social media, ecommerce, marketing, presentations, personal creative work, and image retouching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected input images, and the APIYI bearer token are sent to the APIYI-hosted Gemini image endpoint. <br>
Mitigation: Use the APIYI_API_KEY environment variable where possible, avoid sensitive personal or confidential prompts and images, and confirm the provider/model data-handling terms before use. <br>
Risk: Passing the API key on the command line can expose it through shell history or process inspection. <br>
Mitigation: Prefer APIYI_API_KEY over --api-key and rotate credentials if a key may have been exposed. <br>


## Reference(s): <br>
- [Common usage scenarios](references/scene.md) <br>
- [APIYI service](https://api.apiyi.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIYI_API_KEY or --api-key; supports text-to-image and image-to-image requests, up to 14 input images, 14 aspect ratios, and 1K/2K/4K resolution options.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
