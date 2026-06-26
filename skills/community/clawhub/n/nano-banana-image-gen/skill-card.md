## Description: <br>
Generate and edit images using Pixwith API's Nano Banana 2 model, including text-to-image and image-to-image workflows with up to 4 reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tate-kt](https://clawhub.ai/user/tate-kt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate new images or edit provided images through the Pixwith Nano Banana 2 API. It helps agents check credits, upload user-provided reference images, create generation tasks, poll task status, and return result image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected local images are sent to Pixwith and its upload storage provider. <br>
Mitigation: Avoid sensitive personal or proprietary images unless Pixwith's policies are acceptable for the use case. <br>
Risk: The skill requires a Pixwith API key and consumes paid credits for generation tasks. <br>
Mitigation: Use a dedicated revocable API key, monitor credit use, and inform users of the credit cost before task creation. <br>
Risk: Prompt optimization may translate or rewrite prompts before generation. <br>
Mitigation: Disable prompt optimization when prompt translation or rewriting is not desired. <br>
Risk: Pixwith API response values such as task IDs, upload fields, and result URLs are opaque and can break if changed. <br>
Mitigation: Use API response values exactly as returned when polling tasks, uploading files, and presenting result URLs. <br>


## Reference(s): <br>
- [Pixwith AI](https://pixwith.ai) <br>
- [Pixwith API](https://pixwith.ai/api) <br>
- [Pixwith Pricing](https://pixwith.ai/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/tate-kt/nano-banana-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls, Markdown] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Pixwith task status guidance and image result URLs exactly as provided by the API.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
