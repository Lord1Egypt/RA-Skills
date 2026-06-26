## Description: <br>
Use the Keevx API to convert images to videos with Model V or Model KL, resolutions up to 4K, optional audio generation, task creation, status querying, and batch image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-xiling](https://clawhub.ai/user/baidu-xiling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to prepare Keevx image-to-video API requests, upload local image inputs, choose model and resolution settings, create generation tasks, poll task status, and retrieve generated video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, prompts, and optional callback results are sent to Keevx. <br>
Mitigation: Avoid confidential, regulated, or internal-only media unless Keevx terms and retention are acceptable. <br>
Risk: The agent needs access to a Keevx API key to create and query generation tasks. <br>
Mitigation: Use a dedicated revocable API key, avoid exposing it in logs or shared outputs, and monitor usage costs. <br>
Risk: Callback URLs can expose generated result metadata to endpoints outside the user's control. <br>
Mitigation: Use callback_url only with trusted HTTPS endpoints that the user controls. <br>


## Reference(s): <br>
- [Keevx Documentation](https://docs.keevx.com) <br>
- [Keevx Home](https://www.keevx.com/main/home) <br>
- [ClawHub Skill Page](https://clawhub.ai/baidu-xiling/keevx-image-to-video) <br>
- [Publisher Profile](https://clawhub.ai/user/baidu-xiling) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API requests] <br>
**Output Format:** [Markdown with JSON examples and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands, request bodies, response interpretation, polling guidance, and image upload instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
