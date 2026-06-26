## Description: <br>
GLM V Model helps agents call Zhipu GLM-4V and GLM-4.6V vision models for image and video understanding, multimodal dialogue, and chart analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baokui](https://clawhub.ai/user/baokui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to prepare prompts, image inputs, and example API calls for Zhipu GLM vision-model workflows such as image description, OCR, object recognition, chart analysis, multi-image comparison, and video understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided images, video URLs, and prompts are sent to Zhipu's API. <br>
Mitigation: Do not send confidential images, documents, screenshots, videos, or prompts unless Zhipu's data handling terms are acceptable for the use case. <br>
Risk: Using the skill requires a Zhipu API key and may consume API quota or incur billing. <br>
Mitigation: Provide ZHIPU_API_KEY deliberately, install zai-sdk from a trusted source, and monitor API usage under the relevant Zhipu account. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baokui/glm-v-model) <br>
- [Zhipu AI Open Platform](https://open.bigmodel.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Markdown with Python code examples and plain-text model output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY and sends supplied prompts, images, and video URLs to Zhipu's API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
