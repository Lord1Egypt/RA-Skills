## Description: <br>
Analyzes publicly accessible image URLs with LinkFox's multimodal image recognition API to produce text descriptions, OCR-style extraction, product-image analysis, and visual question answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to send an image URL and a natural-language requirement to LinkFox for image description, OCR-like text extraction, product-image review, screenshot interpretation, and visual question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs, analysis prompts, and the LinkFox API key are sent to LinkFox for processing. <br>
Mitigation: Use only public, non-sensitive image URLs and avoid private, signed, internal, personal, or regulated image links. <br>
Risk: The skill asks the agent to automatically send feedback details to a separate LinkFox endpoint without clear user approval. <br>
Mitigation: Disable the Feedback API path or require explicit approval before sending user comments, outcomes, incident details, or other feedback content. <br>


## Reference(s): <br>
- [Image Recognition API Reference](references/api.md) <br>
- [LinkFox image recognition endpoint](https://tool-gateway.linkfox.com/multimodal/recognizeImage) <br>
- [Skill page](https://clawhub.ai/linkfox-ai/linkfox-multimodal-recognize-image) <br>
- [Publisher profile](https://clawhub.ai/user/linkfox-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with text image-analysis results and optional JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a publicly accessible JPG, JPEG, PNG, GIF, WebP, or BMP image URL and LINKFOXAGENT_API_KEY; imageUrl and requirement are each limited to 1000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
