## Description: <br>
Generate AI images with any model using ImageRouter API (requires API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DaWe35](https://clawhub.ai/user/DaWe35) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and image-generation users use this skill to discover ImageRouter models and compose curl requests for text-to-image, image-to-image, masked editing, and downloading generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, and masks may be sent to ImageRouter under the user's API key. <br>
Mitigation: Avoid uploading private, regulated, or proprietary content unless the provider's handling of that data is acceptable. <br>
Risk: Returned image URLs may point to hosted generated content that users may later download locally. <br>
Mitigation: Review returned download URLs before saving files and only download outputs from expected ImageRouter responses. <br>


## Reference(s): <br>
- [ImageRouter homepage](https://imagerouter.io) <br>
- [ImageRouter image models](https://imagerouter.io/models) <br>
- [ImageRouter API keys](https://imagerouter.io/api-keys) <br>
- [ClawHub skill page](https://clawhub.ai/DaWe35/image-router) <br>
- [Publisher profile](https://clawhub.ai/user/DaWe35) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an ImageRouter API key; image-to-image and mask workflows may upload local image files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
