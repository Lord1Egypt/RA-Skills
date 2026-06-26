## Description: <br>
Generate images from text descriptions using AI models through OATDA's unified API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate AI images, artwork, illustrations, mockups, and concept art through OATDA's unified image-generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OATDA API key for image-generation requests. <br>
Mitigation: Use OATDA_API_KEY from the environment or a properly permissioned credentials file, and do not print or log the full key. <br>
Risk: Image prompts, generated image URLs, and public file URLs supplied as parameters may be visible to OATDA. <br>
Mitigation: Avoid sending sensitive prompts or private file URLs unless the user accepts that service exposure. <br>
Risk: Model IDs and supported image parameters can change over time. <br>
Mitigation: Query the OATDA image model discovery endpoint before generation when a requested model or parameter set is uncertain. <br>


## Reference(s): <br>
- [OATDA](https://oatda.com) <br>
- [OATDA image model discovery endpoint](https://oatda.com/api/v1/llm/models?type=image) <br>
- [OATDA image generation endpoint](https://oatda.com/api/v1/llm/generate-image) <br>
- [ClawHub skill page](https://clawhub.ai/devcsde/oatda-generate-image) <br>
- [Publisher profile](https://clawhub.ai/user/devcsde) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with bash commands, JSON examples, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return one or more generated image URLs and a revised prompt when the OATDA API provides one.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
