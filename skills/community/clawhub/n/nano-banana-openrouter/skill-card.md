## Description: <br>
Generate images from text prompts using Google's Nano Banana Gemini image models through the OpenRouter API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyi0329-pixel](https://clawhub.ai/user/fyi0329-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate images from text prompts through OpenRouter-backed Gemini image models. It supports configurable model selection and aspect ratio inputs for image-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes unsafe credential handling, including a bundled OpenRouter key in a test script. <br>
Mitigation: Use a dedicated OpenRouter key, do not run test-gen.mjs as shipped, and ask the publisher to remove and rotate the bundled key. <br>
Risk: Image prompts are processed by OpenRouter and the selected upstream model provider. <br>
Mitigation: Avoid sending confidential prompts unless that external processing is acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fyi0329-pixel/nano-banana-openrouter) <br>
- [OpenRouter image generation guide](https://openrouter.ai/docs/guides/overview/multimodal/image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, API Calls, configuration, guidance] <br>
**Output Format:** [String containing an image URL, base64 image data, or raw model response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key and sends prompts to OpenRouter and the selected upstream model provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
